from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string, validate_bool
from API.utils.encryption import PasswordHasher
from .Users import UserModel
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime

logger = logging.getLogger('Models.Users.UpdateUser')

class UpdateUsers(BaseCRUD):
    """
    Class to handle updating records in the users table.
    """
    def __init__(self, session):
        super().__init__(session, UserModel)

    def update(self, id, **kwargs):
        """
        Update a UserModel record by ID.
        """
        id = validate_uuid(id, "id")

        if 'email' in kwargs:
            kwargs['email'] = validate_string(kwargs['email'], "email", max_length=500)
        if 'phone' in kwargs:
            kwargs['phone'] = validate_string(kwargs['phone'], "phone", max_length=50)
        if 'password' in kwargs:
            plain_pw = validate_string(kwargs['password'], "password", max_length=255)
            kwargs['password_hash'] = PasswordHasher.hash_password(plain_pw)
            del kwargs['password']  # don't set password field
        if 'first_name' in kwargs:
            kwargs['first_name'] = validate_string(kwargs['first_name'], "first_name", max_length=100)
        if 'last_name' in kwargs:
            kwargs['last_name'] = validate_string(kwargs['last_name'], "last_name", max_length=100)
            kwargs['display_name'] = f'{kwargs["first_name"]} {kwargs["last_name"]}'.strip()
        if 'job_title' in kwargs:
            kwargs['job_title'] = validate_string(kwargs['job_title'], "job_title", max_length=200)
        if 'photo_url' in kwargs:
            kwargs['photo_url'] = validate_string(kwargs['photo_url'], "photo_url", max_length=500)
        if 'country' in kwargs:
            kwargs['country'] = validate_string(kwargs['country'], "country", max_length=100)
        if 'city' in kwargs:
            kwargs['city'] = validate_string(kwargs['city'], "city", max_length=100)
        if 'company_id' in kwargs:
            kwargs['company_id'] = validate_uuid(kwargs['company_id'], "company_id", optional=True)
        if 'is_active' in kwargs:
            kwargs['is_active'] = validate_bool(kwargs['is_active'], "is_active")
        if 'is_blacklisted' in kwargs:
            kwargs['is_blacklisted'] = validate_bool(kwargs['is_blacklisted'], "is_blacklisted")

        logger.info(f"Updating user record with id={id}...")
        try:
            updated_record = super().update(record_id=id, **kwargs)
            if updated_record:
                logger.info(f"User with id={id} updated successfully.")
            return updated_record
        except IntegrityError as e:
            self.session.rollback()
            if 'uq_users_email' in str(e):
                raise ValueError("Email already exists.")
            if 'uq_users_phone' in str(e):
                raise ValueError("Phone already exists.")
            logger.error(f"Failed to update user: {str(e)}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update user: {str(e)}")
            raise
