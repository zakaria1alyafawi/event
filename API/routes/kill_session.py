from flask import request, g
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Sessions.RetrieveSessions import RetrieveSessions
from Models.Sessions.UpdateSessions import UpdateSessions
import logging

logger = logging.getLogger("api.routes.kill_session")

def serialize_session(record):
    """
    Convert a SessionModel object to a JSON-serializable dictionary.
    """
    session_dict = {
        "SessionID": record.SessionID,
        "UserID": record.UserID,
        "Status": record.Status,
        "StartTime": record.StartTime.isoformat() if getattr(record, "StartTime", None) else None,
        "EndTime": record.EndTime.isoformat() if getattr(record, "EndTime", None) else None,
        "Created_at": record.Created_at.isoformat() if getattr(record, "Created_at", None) else None
    }
    # Remove None values and sensitive fields (e.g., Token)
    return {k: v for k, v in session_dict.items() if v is not None}

class KillSessionRoute(BaseRoute):
    """
    Route handler for killing (deactivating) a user session.
    """
    
    def __init__(self):
        """
        Initialize KillSessionRoute with AuthManager.
        """
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("KillSessionRoute initialized")

    def register_routes(self):
        """
        Register the kill_session route endpoint.
        """
        self.bp.route("/kill_session", methods=["GET"])(self.kill_session)

    def kill_session(self):
        """
        Handle POST /kill_session requests to deactivate a user session.
        
        Expects 'Authorization' header with JWT token (e.g., 'Bearer <token>').
        Updates the session's status to 2 (inactive) based on the token.
        
        Returns:
            Response: JSON response with status and updated session data.
        """
        session = self.get_session()
        try:
            # Check Content-Type header (optional for POST with no body, but included for consistency)
            content_type = request.headers.get("Content-Type")
            if content_type and content_type != "application/json":
                logger.warning(f"Invalid Content-Type: {content_type}. Expected application/json or none")
                return error_response("Content-Type must be application/json or omitted", 415)

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

            user_id = auth_result  # Use auth_result as UserID

            # Retrieve session by token
            session_retriever = RetrieveSessions(session)
            session_record = session_retriever.get_by_token(token)
            if not session_record:
                logger.warning(f"No session found for token")
                return error_response("Session not found for token", 404)

            session_record = session_record[0]
            session_id = session_record.SessionID

            # Update session status
            session_updater = UpdateSessions(session)
            updated_session = session_updater.update(
                SessionID=session_id,
                Status=2
            )
            if not updated_session:
                logger.error(f"Failed to update session: SessionID={session_id}")
                return error_response("Failed to kill session", 500)

            logger.info(f"Successfully killed session: SessionID={session_id}, UserID={user_id}")
            session.close()
            return success_response(
                {
                    "message": "Session killed successfully",
                    "session": token
                },
                200
            )

        except ValueError as e:
            logger.warning(f"Validation error in kill_session request: {e}")
            return error_response(str(e), 400)
        except Exception as e:
            logger.error(f"Error processing kill_session request: {e}")
            return error_response("Internal server error", 500)
