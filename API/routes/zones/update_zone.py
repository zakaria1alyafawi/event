from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Zones.UpdateZones import UpdateZones
from Models.Zones.Zones import ZonesModel
from Models.Events.Events import EventsModel
from Models.Utility import validate_uuid
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger("api.routes.zones.update_zone")

class UpdateZoneRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("UpdateZoneRoute initialized")

    def register_routes(self):
        self.bp.route("/update_zone", methods=["POST"])(self.update_zone)

    def update_zone(self):
        session = self.get_session()
        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return error_response("Authorization header required", 401)

            token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
            auth_result = self.auth_manager.authenticate_request(session, token)
            if not auth_result:
                return error_response("Invalid or expired token", 401)
            
            user_id = auth_result
            
            data = request.get_json()
            if not data or 'id' not in data:
                return error_response("Zone ID required in body", 400)

            id = validate_uuid(data['id'], "zone_id")

            update_kwargs = {k: v for k, v in data.items() if k != 'id'}

            update_zones = UpdateZones(session)
            updated_zone = update_zones.update(id, **update_kwargs)

            if not updated_zone:
                return error_response("Zone not found", 404)

            # Fetch full with event
            zone = session.query(ZonesModel).options(joinedload(ZonesModel.event)).filter(ZonesModel.id == id).first()

            event_name = zone.event.title if zone.event else None

            zone_data = {
                "id": str(zone.id),
                "name": zone.name,
                "code": zone.code,
                "capacity": zone.capacity,
                "is_restricted": zone.is_restricted,
                "location_x": zone.location_x,
                "location_y": zone.location_y,
                "event_id": str(zone.event_id),
                "event_name": event_name,
                "created_at": zone.created_at.isoformat() if zone.created_at else None
            }

            logger.info(f"Updated zone {id} by user {user_id}")

            return success_response({
                "message": "Zone updated successfully",
                "zone": zone_data
            })

        except ValueError as ve:
            logger.warning(f"Validation error in update_zone: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in update_zone: {e}")
            return error_response("Internal server error", 500)