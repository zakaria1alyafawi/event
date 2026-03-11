from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Zones.AddZones import AddZones
from Models.Zones.Zones import ZonesModel
from Models.Events.Events import EventsModel
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger("api.routes.zones.add_zone")

class AddZoneRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("AddZoneRoute initialized")

    def register_routes(self):
        self.bp.route("/add_zone", methods=["POST"])(self.add_zone)

    def add_zone(self):
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
            if not data:
                return error_response("JSON body required", 400)

            required_fields = ["event_id", "name", "code"]
            missing = [field for field in required_fields if field not in data]
            if missing:
                return error_response(f"Missing required fields: {', '.join(missing)}", 400)

            kwargs = {
                "event_id": data["event_id"],
                "name": data["name"],
                "code": data["code"]
            }
            for field in ["capacity", "is_restricted", "location_x", "location_y"]:
                if field in data:
                    kwargs[field] = data[field]

            add_zones = AddZones(session)
            new_zone = add_zones.add(**kwargs)

            # Fetch with event
            zone = session.query(ZonesModel).options(joinedload(ZonesModel.event)).filter(ZonesModel.id == new_zone.id).first()

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

            logger.info(f"Added zone {zone.code} by user {user_id}")

            return success_response({
                "message": "Zone created successfully",
                "zone": zone_data
            }, 201)

        except ValueError as ve:
            logger.warning(f"Validation error in add_zone: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in add_zone: {e}")
            return error_response("Internal server error", 500)