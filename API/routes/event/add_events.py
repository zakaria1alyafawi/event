from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Events.AddEvents import AddEvents
from Models.Events.Events import EventsModel
from Models.Users.Users import UserModel
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger("api.routes.event.add_events")

class AddEventsRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("AddEventsRoute initialized")

    def register_routes(self):
        self.bp.route("/add_events", methods=["POST"])(self.add_events)

    def add_events(self):
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

            required_fields = ["slug", "title", "start_date", "end_date", "venue", "organizer_id"]
            missing = [field for field in required_fields if field not in data]
            if missing:
                return error_response(f"Missing required fields: {', '.join(missing)}", 400)

            optional_fields = ["description", "is_published"]
            kwargs = {k: data[k] for k in optional_fields if k in data}
            kwargs.update({
                "slug": data["slug"],
                "title": data["title"],
                "start_date": data["start_date"],
                "end_date": data["end_date"],
                "venue": data["venue"],
                "organizer_id": data["organizer_id"],
                "is_published": data.get("is_published", False)
            })

            add_events = AddEvents(session)
            new_event = add_events.add(**kwargs)

            # Fetch with organizer for name
            event = session.query(EventsModel).options(joinedload(EventsModel.organizer)).filter(EventsModel.id == new_event.id).first()

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

            logger.info(f"Added event {event.slug} by user {user_id}")

            return success_response({
                "message": "Event created successfully",
                "event": event_data
            }, 201)

        except ValueError as ve:
            logger.warning(f"Validation error in add_events: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in add_events: {e}")
            return error_response("Internal server error", 500)