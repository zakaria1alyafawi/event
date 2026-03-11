from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.UpdateUser import UpdateUsers
from Models.Utility import validate_uuid
from Models.Users.RetrieveUsers import RetrieveUsers
import logging

logger = logging.getLogger("api.routes.tenant_management.update_user")

class UpdateUserRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("UpdateUserRoute initialized")

    def register_routes(self):
        self.bp.route("/update_user", methods=["POST"])(self.update_user)

    def update_user(self):
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

            # Prepare kwargs excluding id
            update_kwargs = {k: v for k, v in data.items() if k != 'id'}

            update_users = UpdateUsers(session)
            updated_user = update_users.update(id, **update_kwargs)

            if not updated_user:
                return error_response("User not found or inactive", 404)

            retrieve_users_obj = RetrieveUsers(session)
            profile = retrieve_users_obj.get_full_user_profile(id)
            if not profile:
                return error_response("User not found after update", 404)

            user_data = profile

            logger.info(f"Updated user {id} by user {user_id}")

            return success_response({
                "message": "User updated successfully",
                "user": user_data
            })

        except ValueError as ve:
            logger.warning(f"Validation error in update_user: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in update_user: {e}")
            return error_response("Internal server error", 500)