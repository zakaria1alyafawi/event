from flask import Flask, g
from flask_cors import CORS
import os
from API.config.development import DevelopmentConfig
from API.routes.login import LoginRoute
from API.routes.tenant_management.add_tenant import AddTenantRoute
from API.routes.tenant_management.add_user import AddUserRoute
from API.routes.tenant_management.retrieve_users import RetrieveUsersRoute
from API.routes.tenant_management.get_user import GetUserRoute
from API.routes.tenant_management.update_user import UpdateUserRoute
from API.routes.tenant_management.delete_user import DeleteUserRoute
from API.routes.event.retrieve_events import RetrieveEventsRoute
from API.routes.event.add_events import AddEventsRoute
from API.routes.event.update_events import UpdateEventsRoute
from API.routes.event.delete_events import DeleteEventsRoute
from API.routes.zones.retrieve_zones import RetrieveZonesRoute
from API.routes.zones.add_zone import AddZoneRoute
from API.routes.zones.update_zone import UpdateZoneRoute
from API.routes.zones.delete_zone import DeleteZoneRoute
from API.routes.zones.get_companies_by_zone import GetCompaniesByZoneRoute
from API.routes.companies.retrieve_companies import RetrieveCompaniesRoute
from API.routes.companies.add_company import AddCompanyRoute
from API.routes.companies.update_company import UpdateCompanyRoute
from API.routes.companies.delete_company import DeleteCompanyRoute
from API.routes.staff.qr import QrRoute
from API.routes.staff.get_user_by_access_token import GetUserByAccessTokenRoute
from API.routes.staff.retrieve_connections import RetrieveConnectionsRoute
from API.routes.staff.add_connection import AddConnectionRoute
from API.routes.reset_password import ResetPasswordRoute
from API.routes.kill_session import KillSessionRoute
from API.routes.health import HealthRoute
from API.routes.errors import register_error_handlers
import logging

logger = logging.getLogger("api.init")

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize CORS to allow all origins
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    # Register blueprints
    login_route = LoginRoute()
    add_tenant_route = AddTenantRoute()
    add_user_route = AddUserRoute()
    retrieve_users_route = RetrieveUsersRoute()
    get_user_route = GetUserRoute()
    update_user_route = UpdateUserRoute()
    delete_user_route = DeleteUserRoute()
    retrieve_events_route = RetrieveEventsRoute()
    add_events_route = AddEventsRoute()
    update_events_route = UpdateEventsRoute()
    delete_events_route = DeleteEventsRoute()
    retrieve_zones_route = RetrieveZonesRoute()
    add_zone_route = AddZoneRoute()
    update_zone_route = UpdateZoneRoute()
    delete_zone_route = DeleteZoneRoute()
    get_companies_by_zone_route = GetCompaniesByZoneRoute()
    retrieve_companies_route = RetrieveCompaniesRoute()
    add_company_route = AddCompanyRoute()
    update_company_route = UpdateCompanyRoute()
    delete_company_route = DeleteCompanyRoute()
    reset_password_route = ResetPasswordRoute()
    qr_route = QrRoute()
    get_user_by_access_token_route = GetUserByAccessTokenRoute()
    retrieve_connections_route = RetrieveConnectionsRoute()
    add_connection_route = AddConnectionRoute()
    kill_session_route = KillSessionRoute()
    
    
    app.register_blueprint(login_route.bp, url_prefix="/api/v1")
    app.register_blueprint(add_tenant_route.bp, url_prefix="/api/v1")
    app.register_blueprint(add_user_route.bp, url_prefix="/api/v1")
    app.register_blueprint(retrieve_users_route.bp, url_prefix="/api/v1")
    app.register_blueprint(get_user_route.bp, url_prefix="/api/v1")
    app.register_blueprint(update_user_route.bp, url_prefix="/api/v1")
    app.register_blueprint(delete_user_route.bp, url_prefix="/api/v1")
    app.register_blueprint(retrieve_events_route.bp, url_prefix="/api/v1")
    app.register_blueprint(add_events_route.bp, url_prefix="/api/v1")
    app.register_blueprint(update_events_route.bp, url_prefix="/api/v1")
    app.register_blueprint(delete_events_route.bp, url_prefix="/api/v1")
    app.register_blueprint(retrieve_zones_route.bp, url_prefix="/api/v1")
    app.register_blueprint(add_zone_route.bp, url_prefix="/api/v1")
    app.register_blueprint(update_zone_route.bp, url_prefix="/api/v1")
    app.register_blueprint(delete_zone_route.bp, url_prefix="/api/v1")
    app.register_blueprint(get_companies_by_zone_route.bp, url_prefix="/api/v1")
    app.register_blueprint(retrieve_companies_route.bp, url_prefix="/api/v1")
    app.register_blueprint(add_company_route.bp, url_prefix="/api/v1")
    app.register_blueprint(update_company_route.bp, url_prefix="/api/v1")
    app.register_blueprint(delete_company_route.bp, url_prefix="/api/v1")
    app.register_blueprint(reset_password_route.bp, url_prefix="/api/v1")
    app.register_blueprint(kill_session_route.bp, url_prefix="/api/v1")
    app.register_blueprint(qr_route.bp, url_prefix="/api/v1")
    app.register_blueprint(get_user_by_access_token_route.bp, url_prefix="/api/v1")
    app.register_blueprint(retrieve_connections_route.bp, url_prefix="/api/v1")
    app.register_blueprint(add_connection_route.bp, url_prefix="/api/v1")

    # Register error handlers
    register_error_handlers(app)

    # Initialize sessions list before each request
    @app.before_request
    def before_request():
        g.sessions = []

    # Teardown for session management
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        sessions = getattr(g, 'sessions', [])
        for session in sessions:
            try:
                session.close()
                logger.debug("Closed SQLAlchemy session")
            except Exception as e:
                logger.error(f"Error closing session: {e}")
        g.sessions = []

    return app