from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_enum, validate_string
from .UserTypes import UserTypesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.UserTypes.AddUserTypes')

class AddUserTypes(BaseCRUD):
    """
    Class to handle adding new records to the user_types table.
    """
    def __init__(self, session):
        super().__init__(session, UserTypesModel)

    def add(self, name, description=None):
        """
        Add a new UserTypesModel record.
        Args:
            name (str): user_role enum value.
            description (str): Description.
        """
        user_role_values = ['super_admin', 'event_admin', 'security', 'exhibitor_staff', 'visitor']
        name = validate_enum(name, "name", user_role_values)
        if description:
            description = validate_string(description, "description", max_length=500)

        logger.info(f"Adding UserType record with name={name}...")
        new_record = UserTypesModel(
            name=name,
            description=description
        )
        self.session.add(new_record)
        try:
            self.session.commit()
            logger.info(f"UserType record with name={name} added successfully.")
            return True
        except IntegrityError:
            self.session.rollback()
            logger.warning(f"UserType with name={name} already exists.")
            return False
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding UserType: {e}")
            return False
