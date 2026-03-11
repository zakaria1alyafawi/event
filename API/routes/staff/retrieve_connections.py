from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Connections.RetrieveConnections import RetrieveConnections
import logging

logger = logging.getLogger("api.routes.staff.retrieve_connections")

class RetrieveConnectionsRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("RetrieveConnectionsRoute initialized")

    def register_routes(self):
        self.bp.route("/retrieve_connections", methods=["POST"])(self.retrieve_connections)

    def retrieve_connections(self):
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
                data = {}

            page = max(1, data.get('page', 1))
            limit = min(100, max(1, data.get('limit', 20)))

            retrieve_connections_obj = RetrieveConnections(session)
            result = retrieve_connections_obj.list_paginated(
                user_id=user_id,
                page=page,
                limit=limit
            )

            logger.info(f"Retrieved {len(result['data'])} connections for user {user_id}")

            return success_response(result)

        except ValueError as ve:
            logger.warning(f"Validation error in retrieve_connections: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in retrieve_connections: {e}")
            return error_response("Internal server error", 500)