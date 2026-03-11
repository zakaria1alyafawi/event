from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Users.RetrieveUsers import RetrieveUsers
import logging

logger = logging.getLogger("api.routes.tenant_management.retrieve_users")

class RetrieveUsersRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("RetrieveUsersRoute initialized")

    def register_routes(self):
        self.bp.route("/retrieve_users", methods=["POST"])(self.retrieve_users)

    def retrieve_users(self):
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

            page = max(1, data.get('page', 1))
            limit = min(100, max(1, data.get('limit', 20)))
            search = data.get('search')
            company_id = data.get('company_id')
            role_name = data.get('role_name')

            retrieve_users_obj = RetrieveUsers(session)
            result = retrieve_users_obj.list_paginated(
                search=search,
                company_id=company_id,
                role_name=role_name,
                page=page,
                limit=limit
            )
            logger.info(f"Retrieved {len(result['data'])} users (page {page}, limit {limit}, total {result['total']}) by user {user_id}")

            return success_response(result)

        except ValueError as ve:
            logger.warning(f"Validation error in retrieve_users: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in retrieve_users: {e}")
            return error_response("Internal server error", 500)