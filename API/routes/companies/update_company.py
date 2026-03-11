from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Companies.UpdateCompanies import UpdateCompanies
from Models.Companies.Companies import CompaniesModel
from Models.Zones.Zones import ZonesModel
from Models.Events.Events import EventsModel
from Models.Utility import validate_uuid
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger("api.routes.companies.update_company")

class UpdateCompanyRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("UpdateCompanyRoute initialized")

    def register_routes(self):
        self.bp.route("/update_company", methods=["POST"])(self.update_company)

    def update_company(self):
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
                return error_response("Company ID required in body", 400)

            id = validate_uuid(data['id'], "company_id")

            update_kwargs = {k: v for k, v in data.items() if k != 'id'}

            update_companies = UpdateCompanies(session)
            updated_company = update_companies.update(id, **update_kwargs)

            if not updated_company:
                return error_response("Company not found", 404)

            # Fetch full with joins
            company = session.query(CompaniesModel).options(
                joinedload(CompaniesModel.zone),
                joinedload(CompaniesModel.event)
            ).filter(CompaniesModel.id == id).first()

            zone_name = company.zone.name if company.zone else None
            event_name = company.event.title if company.event else None

            company_data = {
                "id": str(company.id),
                "name": company.name,
                "booth_number": company.booth_number,
                "slug": company.slug,
                "logo_url": company.logo_url,
                "description": company.description,
                "website": company.website,
                "industry": company.industry,
                "email": company.email,
                "phone": company.phone,
                "zone_id": str(company.zone_id) if company.zone_id else None,
                "zone_name": zone_name,
                "event_id": str(company.event_id),
                "event_name": event_name,
                "created_at": company.created_at.isoformat() if company.created_at else None
            }

            logger.info(f"Updated company {id} by user {user_id}")

            return success_response({
                "message": "Company updated successfully",
                "company": company_data
            })

        except ValueError as ve:
            logger.warning(f"Validation error in update_company: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in update_company: {e}")
            return error_response("Internal server error", 500)