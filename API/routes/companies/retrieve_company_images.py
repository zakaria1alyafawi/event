from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from Models.Companies.Companies import CompaniesModel
from sqlalchemy.orm import joinedload
import logging
import os
import base64

logger = logging.getLogger("api.routes.companies.retrieve_company_images")

class RetrieveCompanyImagesRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        logger.info("RetrieveCompanyImagesRoute initialized")

    def register_routes(self):
        self.bp.route("/retrieve_company_images", methods=["GET"])(self.retrieve_company_images)

    def retrieve_company_images(self):
        session = self.get_session()
        try:
            query = session.query(CompaniesModel).filter(
                CompaniesModel.logo_url.isnot(None)
            ).options(
                joinedload(CompaniesModel.zone),
                joinedload(CompaniesModel.event)
            ).order_by(CompaniesModel.created_at.desc())
            companies = query.all()
            company_list = []
            for company in companies:
                zone_name = company.zone.name if company.zone else None
                event_name = company.event.title if company.event else None
                full_path = os.path.join('static', company.logo_url)
                logo_b64 = None
                try:
                    with open(full_path, 'rb') as f:
                        logo_b64 = base64.b64encode(f.read()).decode('utf-8')
                except FileNotFoundError:
                    logger.warning(f"Logo file not found: {full_path}")
                except Exception as img_e:
                    logger.error(f"Error processing image {full_path}: {img_e}")
                company_dict = {
                    "id": str(company.id),
                    "name": company.name,
                    "logo_url": company.logo_url,
                    "logo_base64": logo_b64,
                    "zone_name": zone_name,
                    "event_name": event_name,
                }
                company_list.append(company_dict)
            result = {"companies": company_list}
            logger.info(f"Retrieved {len(company_list)} company logos")
            return success_response(result)
        except Exception as e:
            logger.error(f"Error in retrieve_company_images: {e}")
            return error_response("Internal server error", 500)