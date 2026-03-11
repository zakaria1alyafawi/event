from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_string, validate_uuid, validate_bool, validate_date
from API.utils.encryption import PasswordHasher
from .Users import UserModel
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime

logger = logging.getLogger('Models.Users.AddUser')

class AddUsers(BaseCRUD):
    """
    Class to handle adding new records to the users table.
    """
    def __init__(self, session):
        super().__init__(session, UserModel)

    def add(self, first_name, last_name, password, email=None, phone=None, job_title=None, photo_url=None, country=None, city=None, company_id=None, auth_provider='email', auth_id=None):
        """
        Add a new UserModel record.
        """
        # Validate inputs
        first_name = validate_string(first_name, "first_name", max_length=100)
        last_name = validate_string(last_name, "last_name", max_length=100)
        if email:
            email = validate_string(email, "email", max_length=500)
        if phone:
            phone = validate_string(phone, "phone", max_length=50)
        password = validate_string(password, "password", max_length=255)
        hashed_password = PasswordHasher.hash_password(password)
        if job_title:
            job_title = validate_string(job_title, "job_title", max_length=200)
        if photo_url:
            photo_url = validate_string(photo_url, "photo_url", max_length=500)
        if country:
            country = validate_string(country, "country", max_length=100)
        if city:
            city = validate_string(city, "city", max_length=100)
        if company_id:
            company_id = validate_uuid(company_id, "company_id", optional=True)

        display_name = f'{first_name} {last_name}'.strip()

        logger.info(f"Adding user record with email={email or phone}...")
        new_record = UserModel(
            email=email,
            phone=phone,
            password_hash=hashed_password,
            auth_provider=auth_provider,
            auth_id=auth_id,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            job_title=job_title,
            photo_url=photo_url,
            country=country,
            city=city,
            company_id=company_id,
            is_active=True,
            is_blacklisted=False
        )
        self.session.add(new_record)
        try:
            self.commit()
            logger.info("User added successfully.")
            return new_record
        except IntegrityError as e:
            self.session.rollback()
            if 'uq_users_email' in str(e):
                raise ValueError(f"Email '{email}' already exists.")
            if 'uq_users_phone' in str(e):
                raise ValueError(f"Phone '{phone}' already exists.")
            logger.error(f"Failed to add user: {str(e)}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add user: {str(e)}")
            raise
