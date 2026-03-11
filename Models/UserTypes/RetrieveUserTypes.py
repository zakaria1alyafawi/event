from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_enum
from .UserTypes import UserTypesModel
import logging

logger = logging.getLogger('Models.UserTypes.RetrieveUserTypes')

class RetrieveUserTypes(BaseCRUD):
    """
    Class to handle retrieving records from the user_types table.
    """
    def __init__(self, session):
        super().__init__(session, UserTypesModel)

    def get_all(self):
        """
        Retrieve all UserTypes records.
        """
        logger.info("Retrieving all UserTypes...")
        return self.session.query(UserTypesModel).all()

    def get_by_name(self, name):
        """
        Retrieve UserType by name.
        """
        user_role_values = ['super_admin', 'event_admin', 'security', 'exhibitor_staff', 'visitor']
        name = validate_enum(name, "name", user_role_values)
        logger.info(f"Retrieving UserType by name={name}...")
        return self.session.query(UserTypesModel).filter(UserTypesModel.name == name).first()
