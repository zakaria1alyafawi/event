from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from API.utils.encryption import PasswordHasher
from .Users import UserModel
from Models.UserRoles.UserRoles import UserRolesModel
from Models.UserTypes.UserTypes import UserTypesModel
from sqlalchemy import func, and_, or_, exists
from sqlalchemy.orm import joinedload
from datetime import datetime
import logging

logger = logging.getLogger('Models.Users.RetrieveUsers')

class RetrieveUsers(BaseCRUD):
    """
    Class to handle retrieving records from the users table.
    """
    def __init__(self, session):
        super().__init__(session, UserModel)

    def get_by_email(self, email):
        """
        Retrieve active user by email.
        """
        email = validate_string(email, "email")
        logger.info(f"Retrieving user by email={email}...")
        return self.session.query(UserModel).filter(
            UserModel.email == email,
            UserModel.is_active == True,
            UserModel.deleted_at.is_(None)
        ).first()

    def get_by_access_token(self, token):
        """
        Retrieve active user by access_token if not expired.
        """
        token = validate_uuid(token, "access_token")
        logger.info(f"Retrieving user by access_token={token}...")
        return self.session.query(UserModel).filter(
            UserModel.access_token == token,
            UserModel.is_active == True,
            UserModel.deleted_at.is_(None)
        ).first()

    def validate_login(self, email, plain_password):
        """
        Validate login credentials.
        """
        user = self.get_by_email(email)
        if not user:
            return None
        if PasswordHasher.verify_password(plain_password, user.password_hash):
            return user
        return None

    def get_by_company(self, company_id):
        """
        Retrieve active users by company.
        """
        company_id = validate_uuid(company_id, "company_id")
        logger.info(f"Retrieving users by company_id={company_id}...")
        return self.session.query(UserModel).filter(
            UserModel.company_id == company_id,
            UserModel.is_active == True,
            UserModel.deleted_at.is_(None)
        ).all()

    def get_by_id(self, id):
        """
        Retrieve active user by ID.
        """
        id = validate_uuid(id, "id")
        logger.info(f"Retrieving user by id={id}...")
        return self.session.query(UserModel).filter(
            UserModel.id == id,
            UserModel.is_active == True,
            UserModel.deleted_at.is_(None)
        ).first()

    def get_full_user_profile(self, user_id):
        """
        Retrieve full user profile including roles with event context.
        """
        user_id = validate_uuid(user_id, "user_id")
        logger.info(f"Retrieving full profile for user_id={user_id}...")
        user = self.session.query(UserModel).options(
            joinedload(UserModel.company),
            joinedload(UserModel.user_roles).joinedload(UserRolesModel.role)
        ).filter(
            UserModel.id == user_id,
            UserModel.is_active == True,
            UserModel.deleted_at.is_(None)
        ).first()
        if not user:
            logger.warning(f"User not found for profile: {user_id}")
            return None
        profile = {
            k: str(v) if hasattr(v, "__str__") else v
            for k, v in user.__dict__.items()
            if not k.startswith("_") and k != "password_hash"
        }
        profile["roles"] = [
            {
                "role_id": str(ur.role_id),
                "name": ur.role.name,
                "event_id": str(ur.event_id) if ur.event_id else None
            }
            for ur in user.user_roles
        ]
        profile["company_name"] = user.company.name if user.company else None
        return profile

    def list_paginated(self, search=None, company_id=None, role_name=None, page=1, limit=20):
        '''Paginated list of active users with optional filters.'''
        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(UserModel).filter(
            UserModel.is_active == True,
            UserModel.deleted_at.is_(None)
        )

        if company_id:
            company_id = validate_uuid(company_id, "company_id")
            query = query.filter(UserModel.company_id == company_id)

        if search:
            query = query.filter(
                or_(
                    UserModel.first_name.ilike(f"%{search}%"),
                    UserModel.last_name.ilike(f"%{search}%"),
                    UserModel.email.ilike(f"%{search}%")
                )
            )

        if role_name:
            role_filter = exists().where(
                and_(
                    UserRolesModel.user_id == UserModel.id,
                    UserTypesModel.id == UserRolesModel.role_id,
                    UserTypesModel.name == role_name
                )
            )
            query = query.filter(role_filter)

        total = query.count()

        query = query.options(
            joinedload(UserModel.company),
            joinedload(UserModel.user_roles).joinedload(UserRolesModel.role)
        ).order_by(UserModel.created_at.desc()).offset((page - 1) * limit).limit(limit)

        users = query.all()

        user_list = []
        for user in users:
            roles = [ur.role.name for ur in user.user_roles if ur.role]
            user_dict = {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "display_name": user.display_name,
                "email": user.email,
                "phone": user.phone,
                "job_title": user.job_title,
                "photo_url": user.photo_url,
                "country": user.country,
                "city": user.city,
                "company_id": str(user.company_id) if user.company_id else None,
                "company_name": user.company.name if user.company else None,
                "roles": roles,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            user_list.append(user_dict)

        return {"data": user_list, "total": total, "page": page, "limit": limit}
