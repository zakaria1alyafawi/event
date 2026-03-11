from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Utility import validate_uuid
from Models.Companies.RetrieveCompanies import RetrieveCompanies
import logging

logger = logging.getLogger("api.routes.zones.get_companies_by_zone")

class GetCompaniesByZoneRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("GetCompaniesByZoneRoute initialized")

    def register_routes(self):
        self.bp.route("/get_companies_by_zone", methods=["POST"])(self.get_companies_by_zone)

    def get_companies_by_zone(self):
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
            if not data or 'zone_id' not in data:
                return error_response("Zone ID required in body", 400)

            zone_id = validate_uuid(data['zone_id'], "zone_id")

            page = max(1, data.get('page', 1))
            limit = min(100, max(1, data.get('limit', 20)))
            search = data.get('search')

            retrieve_companies_obj = RetrieveCompanies(session)
            result = retrieve_companies_obj.get_paginated_by_zone(
                zone_id=zone_id,
                search=search,
                page=page,
                limit=limit
            )
            logger.info(f"Retrieved {len(result['data'])} companies for zone {zone_id} (page {page}, limit {limit}, total {result['total']}) by user {user_id}")

            return success_response(result)

        except ValueError as ve:
            logger.warning(f"Validation error in get_companies_by_zone: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in get_companies_by_zone: {e}")
            return error_response("Internal server error", 500)