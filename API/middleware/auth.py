from flask import request
from jose import jwt  # Use python-jose for JWT handling
import os
from datetime import datetime, timedelta, timezone
from API.utils.responses import error_response
import logging
from API.config.base import Config
from Models.Sessions.RetrieveSessions import RetrieveSessions

logger = logging.getLogger("api.middleware.auth")

class AuthManager:
    """
    A class to manage JWT generation and validation for authentication.
    Uses a dedicated JWT_SECRET from environment variables for signing tokens.
    """
    
    def __init__(self):
        """
        Initialize the AuthManager with JWT configuration.
        
        Raises:
            ValueError: If JWT_SECRET is not set in environment variables.
        """
        self.jwt_secret = Config.SECRET_KEY
        if not self.jwt_secret:
            logger.error("JWT_SECRET environment variable is not set")
            raise ValueError("JWT_SECRET must be set in environment variables")
        self.token_expiry_hours = 1
        logger.info("AuthManager initialized")

    def generate_token(self, user_id: str) -> str:
        """
        Generate a JWT for a user with a 1-hour expiry.
        
        Args:
            user_id (int): The user ID to include in the token payload.
        
        Returns:
            str: The encoded JWT.
        
        Raises:
            ValueError: If user_id is not provided.
            Exception: For JWT encoding errors.
        """
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
            logger.debug(f"Generated JWT for user_id={user_id}")
            return token
        except Exception as e:
            logger.error(f"Error generating JWT: {e}")
            raise Exception(f"Failed to generate JWT: {str(e)}")

    def authenticate_request(self, session, token):
        """
        Validate the user by retrieving the session record by token.
        
        Args:
            session: SQLAlchemy session for database queries.
            token (str): JWT token to validate.
        
        Returns:
            int: UserID if the token is valid and session exists.
            None: If the token is invalid, expired, or no session is found.
        """
        try:
            if not token:
                logger.warning("No token provided")
                return None

            session_retriever = RetrieveSessions(session)
            session_record = session_retriever.get_by_token(token)
            if not session_record:
                logger.warning("No session found for token")
                return None

            session_record = session_record[0]
            UserID = session_record.UserID
            EndTime = session_record.EndTime
            Status = session_record.Status
            if datetime.now(timezone.utc) > EndTime or Status == 2:
                logger.warning("Expired token")
                return None

            logger.debug(f"Authenticated request for UserID={UserID}")
            return UserID
        except Exception as e:
            logger.error(f"Error validating token: {e}")
            return None