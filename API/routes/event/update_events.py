from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Events.UpdateEvents import UpdateEvents
from Models.Events.Events import EventsModel
from Models.Users.Users import UserModel
from Models.Utility import validate_uuid
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger("api.routes.event.update_events")

class UpdateEventsRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("UpdateEventsRoute initialized")

    def register_routes(self):
        self.bp.route("/update_events", methods=["POST"])(self.update_events)

    def update_events(self):
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
                return error_response("Event ID required in body", 400)

            id = validate_uuid(data['id'], "event_id")

            update_kwargs = {k: v for k, v in data.items() if k != 'id'}

            update_events = UpdateEvents(session)
            updated_event = update_events.update(id, **update_kwargs)

            if not updated_event:
                return error_response("Event not found", 404)

            # Fetch full with organizer
            event = session.query(EventsModel).options(joinedload(EventsModel.organizer)).filter(EventsModel.id == id).first()

            organizer_name = f"{event.organizer.first_name} {event.organizer.last_name}".strip() if event.organizer else None

            event_data = {
                "id": str(event.id),
                "slug": event.slug,
                "title": event.title,
                "description": event.description,
                "start_date": event.start_date.isoformat() if event.start_date else None,
                "end_date": event.end_date.isoformat() if event.end_date else None,
                "venue": event.venue,
                "organizer_id": str(event.organizer_id) if event.organizer_id else None,
                "organizer_name": organizer_name,
                "is_published": event.is_published,
                "created_at": event.created_at.isoformat() if event.created_at else None
            }

            logger.info(f"Updated event {id} by user {user_id}")

            return success_response({
                "message": "Event updated successfully",
                "event": event_data
            })

        except ValueError as ve:
            logger.warning(f"Validation error in update_events: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in update_events: {e}")
            return error_response("Internal server error", 500)