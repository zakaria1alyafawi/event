from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.AddUser import AddUsers
import logging

logger = logging.getLogger("api.routes.tenant_management.add_tenant")

class AddTenantRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("AddTenantRoute initialized")

    def register_routes(self):
        self.bp.route("/add_tenant", methods=["POST"])(self.add_tenant)

    def add_tenant(self):
        session = self.get_session()
        try:
            data = request.get_json()
            if not data:
                return error_response("JSON body required", 400)

            job_title = data.get("job_title", "").strip().lower()

            # ==================== AUTH LOGIC ====================
            is_visitor_registration = job_title == "visitor"

            if not is_visitor_registration:
                # Normal flow - require authentication
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    return error_response("Authorization header required", 401)

                token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
                auth_result = self.auth_manager.authenticate_request(session, token)
                if not auth_result:
                    return error_response("Invalid or expired token", 401)
                
                user_id = auth_result  # the user who is creating this tenant
                logger.info(f"Adding tenant by authorized user: {user_id}")
            else:
                # Public visitor registration - no auth needed
                user_id = None
                logger.info("Public visitor registration")

            # ==================== VALIDATION ====================
            required_fields = ["first_name", "last_name", "email", "password"]
            missing = [field for field in required_fields if field not in data]
            if missing:
                return error_response(f"Missing required fields: {', '.join(missing)}", 400)

            # Optional fields
            phone = data.get("phone")
            photo_url = data.get("photo_url")
            country = data.get("country")
            city = data.get("city")
            company_id = data.get("company_id")
            auth_provider = data.get("auth_provider", "email")
            auth_id = data.get("auth_id")

            # ==================== CREATE USER ====================
            adder = AddUsers(session)
            new_user = adder.add(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=data["password"],
                phone=phone,
                job_title=data.get("job_title"),   # keep original case
                photo_url=photo_url,
                country=country,
                city=city,
                company_id=company_id,
                auth_provider=auth_provider,
                auth_id=auth_id
            )

            # Serialize response
            user_data = {
                "id": str(new_user.id),
                "email": new_user.email,
                "phone": new_user.phone,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "display_name": new_user.display_name,
                "job_title": new_user.job_title,
                "photo_url": new_user.photo_url,
                "country": new_user.country,
                "city": new_user.city,
                "company_id": str(new_user.company_id) if new_user.company_id else None,
                "is_active": new_user.is_active,
                "created_at": new_user.created_at.isoformat() if new_user.created_at else None
            }

            logger.info(f"Successfully added user {new_user.email} (job_title: {new_user.job_title})")
            
            return success_response({
                "message": "User created successfully",
                "user": user_data
            }, 201)

        except ValueError as ve:
            logger.warning(f"Validation error in add_tenant: {ve}")
            return error_response(str(ve), 400)
        except Exception as e:
            logger.error(f"Error in add_tenant: {e}")
            return error_response("Internal server error", 500)