from flask import request, g
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Users.UpdateUser import UpdateUsers
# from Models.Users.Users import StatusEnum
from API.utils.encryption import PasswordHasher
import logging

logger = logging.getLogger("api.routes.reset_password")

def serialize_user(record):
    """
    Convert a UserModel object to a JSON-serializable dictionary.
    """
    user_dict = {
        "UserID": record.UserID,
        "FirstName": record.FirstName,
        "LastName": record.LastName,
        "Email": record.Email,
        "Phone": record.Phone,
        "Address": record.Address,
        "Status": record.Status.value if isinstance(record.Status) else record.Status,
        "Type": record.Type,
        "TenantID": record.TenantID
    }
    # Remove None values for optional fields (e.g., Address)
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
        Handle POST /reset_password requests to reset a user's password.
        
        Expects 'Authorization' header with JWT token (e.g., 'Bearer <token>').
        Expects JSON body with 'new_password' and optional 'old_password' and 'UserID'.
        If UserID is provided, skips old_password validation and resets password for the specified user.
        If UserID is not provided, uses the authenticated user's ID and validates old_password.
        
        Returns:
            Response: JSON response with status and updated user data (including UserID).
        """
        session = self.get_session()
        try:
            # Check Content-Type header
            content_type = request.headers.get("Content-Type")
            if content_type != "application/json":
                logger.warning(f"Invalid Content-Type: {content_type}. Expected application/json")
                return error_response("Content-Type must be application/json", 415)

            # Check for Authorization in query parameters (warn if misused)
            if "Authorization" in request.args:
                logger.warning("Authorization provided as query parameter; use Authorization header instead")
                return error_response("Authorization must be provided in header, not query parameter", 400)

            # Validate Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                logger.warning("Missing Authorization header")
                return error_response("Authorization header required", 401)

            token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
            auth_result = self.auth_manager.authenticate_request(session, token)
            if auth_result is None:
                logger.warning("Invalid or expired token")
                return error_response("Invalid or expired token", 401)

            auth_user_id = auth_result  # Authenticated user's ID

            # Process request body
            data = request.get_json()
            if not data:
                logger.warning("Missing JSON payload")
                return error_response("JSON payload required", 400)

            new_password = data.get("new_password")
            user_id = data.get("UserID")
            old_password = data.get("old_password") if user_id is None else None

            # Validate inputs
            if not new_password:
                logger.warning("Missing new_password in request body")
                return error_response("new_password is required", 400)
            if not isinstance(new_password, str):
                logger.warning("Invalid new_password format")
                return error_response("new_password must be a string", 400)

            # Determine which user to update
            target_user_id = user_id if user_id is not None else auth_user_id

            # Validate UserID if provided
            if user_id is not None:
                if not isinstance(user_id, int):
                    logger.warning("Invalid UserID format")
                    return error_response("UserID must be an integer", 400)
                
                # Optional: Add permission check
                retriever = RetrieveUsers(session)
                auth_user = retriever.get_active_users_by__id(auth_user_id)
                if not auth_user:
                    logger.warning(f"Authenticated user not found: UserID={auth_user_id}")
                    return error_response(f"Authenticated user with UserID {auth_user_id} not found", 404)
                
                # Placeholder permission check
                if auth_user.Type not in [1,2]:
                    logger.warning(f"UserID={auth_user_id} lacks permission to reset password for UserID={user_id}")
                    return error_response("Insufficient permissions to reset another user's password", 403)

            # Retrieve target user data
            retriever = RetrieveUsers(session)
            retrieved_record = retriever.get_active_users_by__id(target_user_id)
            if not retrieved_record:
                logger.warning(f"User not found: UserID={target_user_id}")
                return error_response(f"User with UserID {target_user_id} not found", 404)

            # Validate old password if UserID is not provided
            if user_id is None:
                if not old_password:
                    logger.warning("Missing old_password in request body")
                    return error_response("old_password is required when UserID is not provided", 400)
                if not isinstance(old_password, str):
                    logger.warning("Invalid old_password format")
                    return error_response("old_password must be a string", 400)
                
                if not PasswordHasher.verify_password(old_password, retrieved_record.Password):
                    logger.warning(f"Invalid old password for UserID={target_user_id}")
                    return error_response("Invalid old password", 401)

            # Update user password (hashed automatically in UpdateUsers)
            updater = UpdateUsers(session)
            updated_record = updater.update(
                UserID=target_user_id,
                Password=new_password,
                Updated_by=auth_user_id
            )
            if not updated_record:
                logger.error(f"Failed to update password for UserID={target_user_id}")
                return error_response("Failed to update password", 500)

            logger.info(f"Successfully reset password for UserID={target_user_id}")
            session.close()
            return success_response(
                {"message": "Password reset successfully", "user": serialize_user(updated_record)},
                200
            )

        except ValueError as e:
            logger.warning(f"Validation error in reset_password request: {e}")
            return error_response(str(e), 400)
        except Exception as e:
            logger.error(f"Error processing reset_password request: {e}")
            return error_response("Internal server error", 500)
