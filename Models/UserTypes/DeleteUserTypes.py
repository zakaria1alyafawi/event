from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .UserTypes import UserTypesModel
import logging

logger = logging.getLogger('Models.UserTypes.DeleteUserTypes')

class DeleteUserTypes(BaseCRUD):
    """
    Class to handle deleting records from the user_types table.
    """
    def __init__(self, session):
        super().__init__(session, UserTypesModel)

    def delete(self, id):
        """
        Delete a UserTypesModel record by ID.
        """
        id = validate_uuid(id, "id")
        logger.info(f"Deleting UserType record with id={id}...")
        success = super().delete(record_id=id)
        if success:
            logger.info(f"UserType with id={id} deleted successfully.")
        return success
