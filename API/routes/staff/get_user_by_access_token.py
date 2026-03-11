from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
import logging

logger = logging.getLogger("api.routes.staff.get_user_by_access_token")

class GetUserByAccessTokenRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("GetUserByAccessTokenRoute initialized")

    def register_routes(self):
        self.bp.route("/get_user_by_access_token", methods=["POST"])(self.get_user_by_access_token)

    def get_user_by_access_token(self):
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
            if not data or 'access_token' not in data:
                return error_response("access_token required in body", 400)

            access_token = data['access_token']

            retrieve_users = RetrieveUsers(session)
            user = retrieve_users.get_by_access_token(access_token)
            if not user:
                return error_response("User not found or inactive/expired token", 404)

            profile = retrieve_users.get_full_user_profile(str(user.id))
            if not profile:
                return error_response("Failed to retrieve profile", 500)

            logger.info(f"Retrieved user by access_token for scanner {user_id}")

            return success_response({
                "user": profile
            })

        except ValueError as ve:
            logger.warning(f"Validation error in get_user_by_access_token: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in get_user_by_access_token: {e}")
            return error_response("Internal server error", 500)