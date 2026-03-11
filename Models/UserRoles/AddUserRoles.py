from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .UserRoles import UserRolesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.UserRoles.AddUserRoles')

class AddUserRoles(BaseCRUD):
    """
    Class to handle adding new records to the user_roles table.
    """
    def __init__(self, session):
        super().__init__(session, UserRolesModel)

    def add_role(self, user_id, role_id, event_id=None):
        """
        Add a user role assignment.
        """
        user_id = validate_uuid(user_id, 'user_id')
        role_id = validate_uuid(role_id, 'role_id')
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')

        # Check if exists
        existing = self.session.query(UserRolesModel).filter(
            UserRolesModel.user_id == user_id,
            UserRolesModel.role_id == role_id,
            UserRolesModel.event_id == event_id
        ).first()
        if existing:
            raise ValueError('Role already assigned to user for this event (or global).')

        logger.info(f'Adding role {role_id} to user {user_id} event {event_id or "global"}')
        new_record = UserRolesModel(
            user_id=user_id,
            role_id=role_id,
            event_id=event_id
        )
        self.session.add(new_record)
        try:
            self.commit()
            logger.info('UserRole added successfully.')
            return new_record
        except IntegrityError:
            self.session.rollback()
            raise ValueError('Role assignment conflict (PK unique).')
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to add UserRole: {str(e)}')
            raise
