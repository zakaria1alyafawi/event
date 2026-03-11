from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .UserRoles import UserRolesModel
from Models.UserTypes.RetrieveUserTypes import RetrieveUserTypes  # for role names
import logging

logger = logging.getLogger('Models.UserRoles.RetrieveUserRoles')

class RetrieveUserRoles(BaseCRUD):
    """
    Class to handle retrieving records from the user_roles table.
    """
    def __init__(self, session):
        super().__init__(session, UserRolesModel)

    def get_user_roles(self, user_id, event_id=None):
        """
        Get roles for a user (event-specific or global).
        """
        user_id = validate_uuid(user_id, 'user_id')
        query = self.session.query(UserRolesModel).filter(UserRolesModel.user_id == user_id)
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')
            query = query.filter(UserRolesModel.event_id == event_id)
        else:
            query = query.filter(UserRolesModel.event_id.is_(None))
        logger.info(f'Retrieving roles for user {user_id} event {event_id or "global"}')
        return query.all()

    def has_role(self, user_id, role_id, event_id=None):
        """
        Check if user has role.
        """
        user_id = validate_uuid(user_id, 'user_id')
        role_id = validate_uuid(role_id, 'role_id')
        query = self.session.query(UserRolesModel).filter(
            UserRolesModel.user_id == user_id,
            UserRolesModel.role_id == role_id
        )
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')
            query = query.filter(UserRolesModel.event_id == event_id)
        else:
            query = query.filter(UserRolesModel.event_id.is_(None))
        count = query.count()
        logger.info(f'User {user_id} has role {role_id}: {count > 0}')
        return count > 0

    def has_role_name(self, user_id, role_name, event_id=None):
        '''Check role by name.'''
        from Models.UserTypes.RetrieveUserTypes import RetrieveUserTypes
        retrieve_user_types = RetrieveUserTypes(self.session)
        role = retrieve_user_types.get_by_name(role_name)
        if not role:
            return False
        return self.has_role(user_id, role.id, event_id)
