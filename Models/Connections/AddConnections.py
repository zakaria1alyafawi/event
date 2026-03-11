from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Connections import ConnectionsModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.Connections.AddConnections')

class AddConnections(BaseCRUD):
    """
    Class to handle adding new records to the connections table.
    """
    def __init__(self, session):
        super().__init__(session, ConnectionsModel)

    def add_connection(self, user_id, connected_to_id, event_id=None, note=None):
        """
        Add a connection between users.
        """
        user_id = validate_uuid(user_id, 'user_id')
        connected_to_id = validate_uuid(connected_to_id, 'connected_to_id')
        if user_id == connected_to_id:
            raise ValueError('Cannot connect to self.')
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')
        if note:
            note = validate_string(note, 'note', max_length=500)

        # Check duplicate
        existing = self.session.query(ConnectionsModel).filter(
            ConnectionsModel.user_id == user_id,
            ConnectionsModel.connected_to_id == connected_to_id,
            ConnectionsModel.event_id == event_id
        ).first()
        if existing:
            raise ValueError('Connection already exists.')

        logger.info(f'Adding connection {user_id} <-> {connected_to_id} event {event_id or "global"}')
        new_record = ConnectionsModel(
            user_id=user_id,
            connected_to_id=connected_to_id,
            event_id=event_id,
            note=note
        )
        self.session.add(new_record)
        try:
            self.commit()
            logger.info('Connection added.')
            return new_record
        except IntegrityError:
            self.session.rollback()
            raise ValueError('Connection conflict (unique constraint).')
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to add connection: {str(e)}')
            raise
