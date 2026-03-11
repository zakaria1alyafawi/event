from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.DeleteUser import DeleteUser
from Models.Utility import validate_uuid
import logging

logger = logging.getLogger("api.routes.tenant_management.delete_user")

class DeleteUserRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("DeleteUserRoute initialized")

    def register_routes(self):
        self.bp.route("/delete_user", methods=["POST"])(self.delete_user)

    def delete_user(self):
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
                return error_response("User ID required in body", 400)

            id = validate_uuid(data['id'], "user_id")

            delete_user = DeleteUser(session)
            success = delete_user.delete(id)

            if success:
                logger.info(f"Deleted user {id} by user {user_id}")
                return success_response({"message": "User deleted successfully"})
            else:
                logger.warning(f"User {id} not found for deletion")
                return error_response("User not found", 404)

        except ValueError as ve:
            logger.warning(f"Validation error in delete_user: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in delete_user: {e}")
            return error_response("Internal server error", 500)