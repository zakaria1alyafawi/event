from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .Connections import ConnectionsModel
import logging

logger = logging.getLogger('Models.Connections.DeleteConnections')

class DeleteConnections(BaseCRUD):
    """
    Class to handle deleting records from the connections table.
    """
    def __init__(self, session):
        super().__init__(session, ConnectionsModel)

    def revoke_connection(self, user_id, connected_to_id, event_id=None):
        """
        Revoke a connection.
        """
        user_id = validate_uuid(user_id, 'user_id')
        connected_to_id = validate_uuid(connected_to_id, 'connected_to_id')
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')

        logger.info(f'Revoking connection {user_id} <-> {connected_to_id} event {event_id or "global"}')
        count = self.session.query(ConnectionsModel).filter(
            ConnectionsModel.user_id == user_id,
            ConnectionsModel.connected_to_id == connected_to_id,
            ConnectionsModel.event_id == event_id
        ).delete()
        if count > 0:
            self.session.commit()
            logger.info(f'Revoked {count} connection(s).')
        return count > 0
