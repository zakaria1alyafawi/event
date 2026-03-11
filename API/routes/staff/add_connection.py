from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Connections.AddConnections import AddConnections
import logging

logger = logging.getLogger("api.routes.staff.add_connection")

class AddConnectionRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("AddConnectionRoute initialized")

    def register_routes(self):
        self.bp.route("/add_connection", methods=["POST"])(self.add_connection)

    def add_connection(self):
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
            if not data or 'friend_access_token' not in data:
                return error_response("friend_access_token required in body", 400)

            friend_access_token = data['friend_access_token']

            retrieve_users = RetrieveUsers(session)
            friend = retrieve_users.get_by_access_token(friend_access_token)
            if not friend:
                return error_response("Invalid friend access_token or inactive user", 400)

            add_connections = AddConnections(session)
            new_connection = add_connections.add_connection(
                user_id=user_id,
                connected_to_id=friend.id,
                event_id=None,  # or from data/auth roles
                note=data.get('note')
            )

            logger.info(f"Added connection {user_id} - {friend.id} by user {user_id}")

            return success_response({
                "message": "Connection added successfully",
                "connection": {
                    "id": str(new_connection.id),
                    "connected_to_id": str(friend.id),
                    "scanned_at": new_connection.scanned_at.isoformat() if new_connection.scanned_at else None
                }
            }, 201)

        except ValueError as ve:
            logger.warning(f"Validation error in add_connection: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in add_connection: {e}")
            return error_response("Internal server error", 500)