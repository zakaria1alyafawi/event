from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Connections import ConnectionsModel
import logging

logger = logging.getLogger('Models.Connections.UpdateConnections')

class UpdateConnections(BaseCRUD):
    """
    Class to handle updating records in the connections table.
    """
    def __init__(self, session):
        super().__init__(session, ConnectionsModel)

    def update_note(self, id, note):
        """
        Update connection note.
        """
        id = validate_uuid(id, 'id')
        note = validate_string(note, 'note', max_length=500)

        logger.info(f'Updating connection {id} note')
        record = self.session.query(ConnectionsModel).filter(ConnectionsModel.id == id).first()
        if not record:
            return None
        record.note = note
        self.session.commit()
        return record
