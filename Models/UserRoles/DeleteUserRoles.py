from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .UserRoles import UserRolesModel
import logging

logger = logging.getLogger('Models.UserRoles.DeleteUserRoles')

class DeleteUserRoles(BaseCRUD):
    """
    Class to handle deleting records from the user_roles table.
    """
    def __init__(self, session):
        super().__init__(session, UserRolesModel)

    def revoke_role(self, user_id, role_id, event_id=None):
        """
        Revoke a user role.
        """
        user_id = validate_uuid(user_id, 'user_id')
        role_id = validate_uuid(role_id, 'role_id')
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')

        logger.info(f'Revoking role {role_id} from user {user_id} event {event_id or "global"}')
        count = self.session.query(UserRolesModel).filter(
            UserRolesModel.user_id == user_id,
            UserRolesModel.role_id == role_id,
            UserRolesModel.event_id == event_id
        ).delete()
        if count > 0:
            self.session.commit()
            logger.info(f'Revoked {count} role assignment(s).')
        return count > 0
