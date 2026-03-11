from flask import request, g
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Users.UpdateUser import UpdateUsers
from Models.UserRoles.RetrieveUserRoles import RetrieveUserRoles
from Models.Utility import validate_uuid
from API.utils.encryption import PasswordHasher
import logging

logger = logging.getLogger("api.routes.reset_password")

def serialize_user(record):
    """
    Convert a UserModel object to a JSON-serializable dictionary.
    """
    user_dict = {
        "id": str(record.id),
        "first_name": record.first_name,
        "last_name": record.last_name,
        "email": record.email,
        "phone": record.phone,
        "job_title": record.job_title,
        "photo_url": record.photo_url,
        "country": record.country,
        "city": record.city,
        "company_id": str(record.company_id) if record.company_id else None,
        "is_active": record.is_active,
        "is_blacklisted": record.is_blacklisted,
        "auth_provider": record.auth_provider,
        "auth_id": record.auth_id if record.auth_id else None
    }
    # Remove None values
    return {k: v for k, v in user_dict.items() if v is not None}

class ResetPasswordRoute(BaseRoute):
    """
    Route handler for resetting a user's password.
    """
    
    def __init__(self):
        """
        Initialize ResetPasswordRoute with AuthManager.
        """
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("ResetPasswordRoute initialized")

    def register_routes(self):
        """
        Register the reset_password route endpoint.
        """
        self.bp.route("/reset_password", methods=["POST"])(self.reset_password)

    def reset_password(self):
        """
        Handle POST /api/v1/reset_password requests to reset a user's password.
        
        Expects 'Authorization' header with JWT token.
        Expects JSON body with 'new_password' required, 'user_id' optional (UUID), 'old_password' for self-reset.
        
        Self-reset: no user_id, requires old_password.
        Admin reset: user_id provided, requires super_admin role, no old_password.
        
        Returns:
            JSON response with status and updated user data.
        """
        session = self.get_session()
        try:
            # Validate Content-Type
            content_type = request.headers.get("Content-Type")
            if content_type != "application/json":
                logger.warning(f"Invalid Content-Type: {content_type}")
                return error_response("Content-Type must be application/json", 415)

            # Warn if Authorization in query params
            if "Authorization" in request.args:
                logger.warning("Authorization in query param")
                return error_response("Use Authorization header", 400)

            # Authenticate
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return error_response("Authorization header required", 401)

            token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
            auth_result = self.auth_manager.authenticate_request(session, token)
            if auth_result is None:
                return error_response("Invalid or expired token", 401)

            auth_user_id = auth_result

            # Parse body
            data = request.get_json()
            if not data:
                return error_response("JSON payload required", 400)

            new_password = data.get("new_password")
            user_id = data.get("user_id")
            old_password = data.get("old_password")

            if not new_password or not isinstance(new_password, str):
                return error_response("new_password must be a non-empty string", 400)

            target_user_id = user_id if user_id is not None else auth_user_id

            retriever = RetrieveUsers(session)

            # Permission check if resetting other user
            if user_id is not None:
                user_id = validate_uuid(user_id, "user_id")
                retrieve_user_roles = RetrieveUserRoles(session)
                if not retrieve_user_roles.has_role_name(auth_user_id, "super_admin"):
                    return error_response("Only super_admin can reset other users' passwords", 403)

            # Get target user
            retrieved_record = retriever.get_by_id(target_user_id)
            if not retrieved_record:
                return error_response(f"Active user not found: {target_user_id}", 404)

            # Verify old password for self-reset
            if user_id is None:
                if not old_password or not isinstance(old_password, str):
                    return error_response("old_password required for self-reset", 400)
                if not PasswordHasher.verify_password(old_password, retrieved_record.password_hash):
                    return error_response("Invalid old password", 401)

            # Update password
            updater = UpdateUsers(session)
            updated_record = updater.update(target_user_id, Password=new_password)
            if not updated_record:
                logger.error(f"Failed to update password for {target_user_id}")
                return error_response("Failed to update password", 500)

            logger.info(f"Password reset for user {target_user_id} by {auth_user_id}")
            return success_response(
                {"message": "Password reset successfully", "user": serialize_user(updated_record)},
                200
            )

        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return error_response(str(e), 400)
        except Exception as e:
            logger.error(f"Error in reset_password: {e}")
            return error_response("Internal server error", 500)
