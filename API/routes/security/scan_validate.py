from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Zones.RetrieveZones import RetrieveZones
from Models.Events.RetrieveEvents import RetrieveEvents
from Models.ZoneScans.RetrieveZoneScans import RetrieveZoneScans
from Models.EventAttendance.RetrieveEventAttendance import RetrieveEventAttendance
from Models.ZoneScans.AddZoneScans import AddZoneScans
from Models.EventAttendance.AddEventAttendance import AddEventAttendance
from Models.UserRoles.RetrieveUserRoles import RetrieveUserRoles
from Models.Utility import validate_uuid
import logging

logger = logging.getLogger("api.routes.security.scan_validate")


class ScanValidateRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("ScanValidateRoute initialized")

    def register_routes(self):
        self.bp.route("/scan_validate", methods=["POST"])(self.scan_validate)

    def scan_validate(self):
        session = self.get_session()
        try:
            # ====================== AUTHENTICATION ======================
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return error_response("Authorization header required", 401)

            token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
            auth_result = self.auth_manager.authenticate_request(session, token)
            if not auth_result:
                return error_response("Invalid or expired token", 401)

            scanner_id = auth_result

            # Check scanner has security role
            retrieve_user_roles = RetrieveUserRoles(session)
            if not retrieve_user_roles.has_role_name(scanner_id, 'security'):
                return error_response("Scanner must have security role", 403)

            # ====================== INPUT VALIDATION ======================
            data = request.get_json()
            if not data:
                return error_response("JSON body required", 400)

            access_token = data.get('access_token')
            event_id = data.get('event_id')
            zone_id = data.get('zone_id')
            action = data.get('action')

            if not access_token or not action:
                return error_response("access_token and action are required", 400)

            if bool(event_id) == bool(zone_id):
                return error_response("Exactly one of event_id or zone_id is required", 400)

            access_token = validate_uuid(access_token, 'access_token')
            if event_id:
                event_id = validate_uuid(event_id, 'event_id')
            if zone_id:
                zone_id = validate_uuid(zone_id, 'zone_id')

            if action not in ['enter', 'exit']:
                return error_response("action must be 'enter' or 'exit'", 400)

            # ====================== GET USER ======================
            retrieve_users = RetrieveUsers(session)
            user = retrieve_users.get_by_access_token(access_token)
            if not user:
                return success_response({
                    "success": False,
                    "status": "invalid_access_token",
                    "message": "Invalid or inactive access token"
                })

            # ====================== RESOLVE TARGET (Event or Zone) ======================
            target_type = None
            target_id = None
            event = None
            zone = None

            if event_id:
                target_type = 'event'
                target_id = event_id
                event = RetrieveEvents(session).get_by_id(event_id)
                if not event:
                    return success_response({
                        "success": False,
                        "status": "event_not_found",
                        "message": "Event not found"
                    })
            else:
                target_type = 'zone'
                retrieve_zones = RetrieveZones(session)
                zone = retrieve_zones.get_by_id(zone_id)
                if not zone:
                    return success_response({
                        "success": False,
                        "status": "zone_not_found",
                        "message": "Zone not found"
                    })
                event = RetrieveEvents(session).get_by_id(zone.event_id)
                if not event:
                    return success_response({
                        "success": False,
                        "status": "event_not_found",
                        "message": "Event not found for this zone"
                    })
                target_id = zone_id

            # ====================== DUPLICATE / TOGGLE CHECK ======================
            latest = None
            if event_id:
                retrieve_target = RetrieveEventAttendance(session)
                latest = retrieve_target.get_last_attendance(user.id, event_id)
            else:
                retrieve_target = RetrieveZoneScans(session)
                latest = retrieve_target.get_last_scan(user.id, zone_id)

            if latest and latest.action == action:
                deny_status = f"{target_type}_already_{action}"
                return success_response({
                    "success": False,
                    "status": deny_status,
                    "message": f"User already performed {action} for this {target_type}"
                })

            # ====================== RECORD THE SCAN ======================
            if event_id:
                add_event_att = AddEventAttendance(session)
                add_event_att.record_scan(user.id, event_id, action, scanner_id)
            else:
                add_zone_scans = AddZoneScans(session)
                add_zone_scans.record_scan(user.id, zone_id, action, scanner_id)

            logger.info(f"Scan {action} successful for user {user.id} on {target_type} by scanner {scanner_id}")

            # ====================== SUCCESS RESPONSE ======================
            return success_response({
                "success": True,
                "status": f"{target_type}_{action}_ok",
                "message": f"{action.capitalize()} {target_type} recorded successfully",
                "user": {
                    "first_name": user.first_name,
                    "photo_url": user.photo_url,
                    "id": str(user.id)   # optional but useful
                }
            })

        except ValueError as ve:
            logger.warning(f"Validation error in scan_validate: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in scan_validate: {e}", exc_info=True)
            return error_response("Internal server error", 500)