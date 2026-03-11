from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .UserRoles import UserRolesModel
import logging

logger = logging.getLogger('Models.UserRoles.UpdateUserRoles')

class UpdateUserRoles(BaseCRUD):
    """
    Class to handle updating records in the user_roles table (limited, mostly immutable).
    """
    def __init__(self, session):
        super().__init__(session, UserRolesModel)

    def update(self, user_id, role_id, event_id=None, **kwargs):
        """
        Update a UserRoles record (rarely used).
        """
        user_id = validate_uuid(user_id, 'user_id')
        role_id = validate_uuid(role_id, 'role_id')
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')

        record = self.session.query(UserRolesModel).filter(
            UserRolesModel.user_id == user_id,
            UserRolesModel.role_id == role_id,
            UserRolesModel.event_id == event_id
        ).first()
        if not record:
            logger.warning(f'UserRole not found for user {user_id}, role {role_id}, event {event_id}')
            return None

        for key, value in kwargs.items():
            setattr(record, key, value)

        self.session.commit()
        logger.info(f'UserRole updated for user {user_id}, role {role_id}')
        return record
