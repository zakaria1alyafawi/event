from flask import jsonify
from API.utils.responses import error_response
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("api.routes.errors")

def register_error_handlers(app):
    """
    Register error handlers for the Flask app to handle various HTTP and custom errors.
    """
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad Request: {str(error)}")
        return error_response("Bad request: Invalid input provided", 400)

    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"Unauthorized: {str(error)}")
        return error_response("Unauthorized: Authentication required", 401)

    @app.errorhandler(403)
    def forbidden(error):
        logger.warning(f"Forbidden: {str(error)}")
        return error_response("Forbidden: Access denied", 403)

    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"Not Found: {str(error)}")
        return error_response("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.warning(f"Method Not Allowed: {str(error)}")
        return error_response("Method not allowed", 405)

    @app.errorhandler(429)
    def too_many_requests(error):
        logger.warning(f"Too Many Requests: {str(error)}")
        return error_response("Too many requests: Rate limit exceeded", 429)

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal Server Error: {str(error)}")
        return error_response("Internal server error", 500)

    @app.errorhandler(503)
    def service_unavailable(error):
        logger.error(f"Service Unavailable: {str(error)}")
        return error_response("Service unavailable: Try again later", 503)

    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        logger.error(f"Database Error: {str(error)}")
        return error_response("Database error occurred", 500)

    @app.errorhandler(ValueError)
    def validation_error(error):
        logger.warning(f"Validation Error: {str(error)}")
        return error_response(f"Validation error: {str(error)}", 400)