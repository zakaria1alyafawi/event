from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_enum, validate_string
from .UserTypes import UserTypesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.UserTypes.UpdateUserTypes')

class UpdateUserTypes(BaseCRUD):
    """
    Class to handle updating records in the user_types table.
    """
    def __init__(self, session):
        super().__init__(session, UserTypesModel)

    def update(self, id, **kwargs):
        """
        Update a UserTypesModel record by ID.
        """
        id = validate_uuid(id, "id")

        user_role_values = ['super_admin', 'event_admin', 'security', 'exhibitor_staff', 'visitor']
        if 'name' in kwargs:
            kwargs['name'] = validate_enum(kwargs['name'], "name", user_role_values)
        if 'description' in kwargs:
            kwargs['description'] = validate_string(kwargs['description'], "description", max_length=500)

        logger.info(f"Updating UserType record with id={id}...")
        try:
            updated_record = super().update(record_id=id, **kwargs)
            if updated_record:
                logger.info(f"UserType with id={id} updated successfully.")
            return updated_record
        except IntegrityError as e:
            self.session.rollback()
            if "uq_user_types_name" in str(e):
                raise ValueError(f"UserType name already exists.")
            logger.error(f"Failed to update UserType: {str(e)}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update UserType: {str(e)}")
            raise
