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
from Models.Companies.RetrieveCompanies import RetrieveCompanies
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
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return error_response("Authorization header required", 401)

            token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
            auth_result = self.auth_manager.authenticate_request(session, token)
            if not auth_result:
                return error_response("Invalid or expired token", 401)
            
            scanner_id = auth_result

            # Check scanner role security
            retrieve_user_roles = RetrieveUserRoles(session)
            if not retrieve_user_roles.has_role_name(scanner_id, 'security'):
                return error_response("Scanner must have security role", 403)

            data = request.get_json()
            if not data:
                return error_response("JSON body required", 400)

            access_token = data.get('access_token')
            zone_id = data.get('zone_id')
            event_id = data.get('event_id')
            action = data.get('action')

            if not access_token or not zone_id or not action:
                return error_response("access_token, zone_id, action required", 400)

            access_token = validate_uuid(access_token, 'access_token')
            zone_id = validate_uuid(zone_id, 'zone_id')
            if event_id:
                event_id = validate_uuid(event_id, 'event_id')
            if action not in ['enter', 'exit']:
                return error_response("action must be 'enter' or 'exit'", 400)

            # 1. Get user by access_token
            retrieve_users = RetrieveUsers(session)
            user = retrieve_users.get_by_access_token(access_token)
            if not user:
                return error_response("Invalid access_token or inactive user", 400, status='inactive')

            # 2. Get zone
            retrieve_zones = RetrieveZones(session)
            zone = retrieve_zones.get_by_id(zone_id)
            if not zone:
                return error_response("Zone not found", 404)

            # 3. Get event
            event = RetrieveEvents(session).get_by_id(event_id or zone.event_id)
            if not event:
                return error_response("Event not found", 404)

            # 4. Check user roles exhib/visitor for event
            user_roles = retrieve_user_roles.get_user_roles(user.id, event.id)
            user_role_names = [r['type_name'] for r in user_roles]
            if not any(role in ['exhibitor_staff', 'visitor'] for role in user_role_names):
                return error_response("User role not authorized for event", 403, status='denied_role')

            # 5. Check company match event/zone companies
            retrieve_companies = RetrieveCompanies(session)
            event_companies = set(c.id for c in retrieve_companies.get_by_event(event.id))
            zone_companies = set(c.id for c in retrieve_companies.get_by_zone(zone.id))
            if user.company_id not in event_companies or user.company_id not in zone_companies:
                return error_response("User company not in event/zone", 403, status='denied_role')

            # 6. Last scans
            retrieve_zone_scans = RetrieveZoneScans(session)
            last_zone_scan = retrieve_zone_scans.get_last_scan(user.id, zone.id)
            retrieve_event_att = RetrieveEventAttendance(session)
            last_event_att = retrieve_event_att.get_last_attendance(user.id, event.id)

            status = 'ok'
            if action == 'enter':
                if last_zone_scan and last_zone_scan.action == 'enter':
                    status = 'already_in_zone'
                if last_event_att and last_event_att.action == 'enter':
                    status = 'already_in_event'
                # Capacity check
                if zone.capacity:
                    occupancy = retrieve_zone_scans.get_zone_occupancy(zone.id)  # implement if needed
                    if occupancy >= zone.capacity:
                        status = 'capacity_full'
            elif action == 'exit':
                if last_zone_scan and last_zone_scan.action == 'exit':
                    status = 'already_out_zone'

            if status != 'ok':
                return error_response(status, 400, status=status)

            # 7. Add scans
            add_zone_scans = AddZoneScans(session)
            add_zone_scans.record_scan(user.id, zone.id, scanner_id, action)

            add_event_att = AddEventAttendance(session)
            add_event_att.record_scan(user.id, event.id, scanner_id, action)

            logger.info(f"Scan {action} for user {user.id} zone {zone.id} by scanner {scanner_id}")

            return success_response({
                "success": True,
                "status": f"{action}_ok",
                "message": f"{action.capitalize()} successful",
                "user": {
                    "first_name": user.first_name,
                    "photo_url": user.photo_url,
                    "roles": user_role_names
                }
            })

        except ValueError as ve:
            logger.warning(f"Validation error in scan_validate: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in scan_validate: {e}")
            return error_response("Internal server error", 500)