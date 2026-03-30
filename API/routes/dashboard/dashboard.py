from flask import request
from API.routes.base import BaseRoute
from API.middleware.auth import AuthManager
from API.utils.responses import success_response, error_response
from Models.Users.RetrieveUsers import RetrieveUsers
from Models.Events.RetrieveEvents import RetrieveEvents
from Models.Zones.RetrieveZones import RetrieveZones
from Models.Companies.Companies import CompaniesModel
from Models.Companies.RetrieveCompanies import RetrieveCompanies
from Models.EventAttendance.RetrieveEventAttendance import RetrieveEventAttendance
from Models.ZoneScans.RetrieveZoneScans import RetrieveZoneScans
import logging

logger = logging.getLogger("api.routes.dashboard")

class DashboardRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.register_routes()

    def register_routes(self):
        self.bp.route("/dashboard", methods=["GET"])(self.dashboard_handler)

    def dashboard_handler(self):
        session = self.get_session()
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return error_response("Authorization header required", 401)

        token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
        auth_result = self.auth_manager.authenticate_request(session, token)
        if not auth_result:
            return error_response("Invalid or expired token", 401)
        
        user_id = auth_result

        retrieve_users = RetrieveUsers(session)
        users_by_role = retrieve_users.count_by_role_grouped()

        retrieve_events = RetrieveEvents(session)
        total_events = retrieve_events.count_active()

        retrieve_zones = RetrieveZones(session)
        total_zones = retrieve_zones.count_active()

        retrieve_companies = RetrieveCompanies(session)
        total_companies = retrieve_companies.count_active() if hasattr(retrieve_companies, 'count_active') else session.query(CompaniesModel).count()

        retrieve_att = RetrieveEventAttendance(session)
        attendance_daily = retrieve_att.get_daily_counts()

        retrieve_scans = RetrieveZoneScans(session)
        scans_daily = retrieve_scans.get_daily_counts()

        data = {
            "users_by_role": users_by_role,
            "total_events": total_events,
            "total_zones": total_zones,
            "total_companies": total_companies,
            "attendance_daily": attendance_daily,
            "scans_daily": scans_daily
        }
        return success_response(data)