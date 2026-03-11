from flask import request, jsonify, g
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Sessions.AddSessions import AddSessions
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("api.routes.login")

class LoginRoute(BaseRoute):
    """
    Route handler for user login, validating credentials and creating sessions.
    """
    
    def __init__(self):
        """
        Initialize LoginRoute with PasswordEncryptor and AuthManager.
        """
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("LoginRoute initialized")

    def register_routes(self):
        """
        Register the login route endpoint.
        """
        self.bp.route("/login", methods=["POST"])(self.login)

    def login(self):
        """
        Handle POST /login requests to authenticate users and create sessions.
        
        Expects JSON payload with 'email' and 'password' and Content-Type: application/json.
        Returns a JWT and success message on valid credentials.
        
        Returns:
            Response: JSON response with status, message, and token (if successful).
        """
        session = self.get_session()
        try:
            # Check Content-Type header
            content_type = request.headers.get("Content-Type")
            if content_type != "application/json":
                logger.warning(f"Invalid Content-Type: {content_type}. Expected application/json")
                return error_response("Content-Type must be application/json", 415)

            data = request.get_json()
            if not data:
                logger.warning("Missing JSON payload in login request")
                return error_response("JSON payload required", 400)

            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                logger.warning("Missing email or password in login request")
                return error_response("Email and password are required", 400)

            retriever = RetrieveUsers(session)
            user = retriever.validate_login(email, password)

            if user:
                # Generate JWT token
                token = self.auth_manager.generate_token(str(user.id))
                # Insert session record
                session_manager = AddSessions(session)
                session_manager.add(
                    UserID=user.id,
                    StartTime=datetime.now(),
                    EndTime=datetime.now() + timedelta(hours=1),
                    Token=token,
                    Status=1,
                    Created_at=datetime.utcnow()
                )
                
                profile = retriever.get_full_user_profile(str(user.id))
                if not profile:
                    logger.error(f"Profile not found for user {user.id}")
                    session.close()
                    return error_response("Failed to retrieve user profile", 500)
                logger.info(f"Successful login for email={email}")
                session.close()
                return success_response(
                    {
                        "message": "Login successful",
                        "token": token,
                        **profile
                    },
                    200
                )
            else:
                logger.warning(f"Invalid credentials for email={email}")
                return error_response("Invalid email or password", 401)

        except ValueError as e:
            logger.error(f"Validation error in login request: {e}")
            return error_response(str(e), 400)
        except Exception as e:
            logger.error(f"Error processing login request: {e}")
            return error_response("Internal server error", 500)
