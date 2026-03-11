from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .Users import UserModel
from datetime import datetime
import logging

logger = logging.getLogger('Models.Users.DeleteUser')

class DeleteUser(BaseCRUD):
    """
    Class to handle deleting records from the users table (soft delete).
    """
    def __init__(self, session):
        super().__init__(session, UserModel)

    def delete(self, id):
        """
        Soft delete a UserModel record by ID (set deleted_at, is_active=False).
        """
        id = validate_uuid(id, "id")

        logger.info(f"Soft deleting user with id={id}...")
        user = self.session.query(UserModel).filter(UserModel.id == id).first()
        if not user:
            logger.warning(f"User with id={id} not found.")
            return False
        user.is_active = False
        user.deleted_at = datetime.utcnow()
        try:
            self.session.commit()
            logger.info(f"User with id={id} soft deleted.")
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to soft delete user: {str(e)}")
            return False
