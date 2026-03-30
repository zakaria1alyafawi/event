from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Companies.AddCompanies import AddCompanies
from Models.Companies.Companies import CompaniesModel
from Models.Zones.Zones import ZonesModel
from Models.Events.Events import EventsModel
from sqlalchemy.orm import joinedload
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
import io
import logging

logger = logging.getLogger("api.routes.companies.add_company")

class AddCompanyRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("AddCompanyRoute initialized")

    def register_routes(self):
        self.bp.route("/add_company", methods=["POST"])(self.add_company)

    def add_company(self):
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
            
            if 'multipart' in request.content_type.lower():
                form_data = request.form.to_dict()
                logo_file = request.files.get('logo')
            else:
                form_data = request.get_json() or {}
                logo_file = None

            required_fields = ["event_id", "zone_id", "name"]
            missing = [field for field in required_fields if field not in form_data]
            if missing:
                return error_response(f"Missing required fields: {', '.join(missing)}", 400)

            kwargs = {
                "event_id": form_data["event_id"],
                "zone_id": form_data["zone_id"],
                "name": form_data["name"]
            }
            for field in ["booth_number", "slug", "logo_url", "description", "website", "industry", "email", "phone"]:
                if field in form_data:
                    kwargs[field] = form_data[field]

            if logo_file and logo_file.filename:
                try:
                    logo_file.seek(0)
                    image = Image.open(io.BytesIO(logo_file.read()))
                    allowed_formats = ('JPEG', 'PNG', 'GIF', 'WEBP')
                    if image.format not in allowed_formats:
                        return error_response("Invalid image format. Allowed: JPEG, PNG, GIF, WEBP", 400)
                    ext = f".{image.format.lower()}"
                    filename = f"{uuid.uuid4().hex}{ext}"
                    path = os.path.join('static', 'companies', 'logos', filename)
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    image.save(path)
                    kwargs['logo_url'] = f"companies/logos/{filename}"
                except Exception as e:
                    logger.error(f"Image processing error: {e}")
                    return error_response("Invalid image file", 400)

            add_companies = AddCompanies(session)
            new_company = add_companies.add(**kwargs)

            # Fetch with joins
            company = session.query(CompaniesModel).options(
                joinedload(CompaniesModel.zone),
                joinedload(CompaniesModel.event)
            ).filter(CompaniesModel.id == new_company.id).first()

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
                "zone_id": str(company.zone_id),
                "zone_name": zone_name,
                "event_id": str(company.event_id),
                "event_name": event_name,
                "created_at": company.created_at.isoformat() if company.created_at else None
            }

            logger.info(f"Added company {company.name} by user {user_id}")

            return success_response({
                "message": "Company created successfully",
                "company": company_data
            }, 201)

        except ValueError as ve:
            logger.warning(f"Validation error in add_company: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in add_company: {e}")
            return error_response("Internal server error", 500)