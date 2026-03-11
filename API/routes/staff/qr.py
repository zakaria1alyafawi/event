from flask import request
from API.routes.base import BaseRoute
from API.utils.responses import success_response, error_response
from API.middleware.auth import AuthManager
from Models.Users.RetrieveUsers import RetrieveUsers
import qrcode
from io import BytesIO
import base64
import logging

logger = logging.getLogger("api.routes.staff.qr")

class QrRoute(BaseRoute):
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        logger.info("QrRoute initialized")

    def register_routes(self):
        self.bp.route("/qr", methods=["POST"])(self.qr)

    def qr(self):
        session = self.get_session()
        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return error_response("Authorization header required", 401)

            token = auth_header.replace("Bearer ", "", 1) if auth_header.startswith("Bearer ") else auth_header
            auth_result = self.auth_manager.authenticate_request(session, token)
            if not auth_result:
                return error_response("Invalid or expired token", 401)
            
            user_id = auth_result

            retrieve_users = RetrieveUsers(session)
            user = retrieve_users.get_by_id(user_id)
            if not user:
                return error_response("User not found", 404)

            # Generate QR for access_token
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(user.access_token))
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            logger.info(f"Generated QR for user {user_id}")

            return success_response({
                "qr_code": f"data:image/png;base64,{img_str}"
            })

        except Exception as e:
            logger.error(f"Error in qr: {e}")
            return error_response("Internal server error", 500)