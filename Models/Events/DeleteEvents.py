from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .Events import EventsModel
import logging
from datetime import datetime

logger = logging.getLogger('Models.Events.DeleteEvents')

class DeleteEvents(BaseCRUD):
    """
    Class to handle soft deleting records from the events table.
    """
    def __init__(self, session):
        super().__init__(session, EventsModel)

    def delete(self, id):
        """
        Soft delete an EventsModel record by ID.
        """
        id = validate_uuid(id, 'id')
        event = self.session.query(EventsModel).filter(EventsModel.id == id).first()
        if not event:
            logger.warning(f'Event {id} not found.')
            return False
        event.deleted_at = datetime.utcnow()
        try:
            self.session.commit()
            logger.info(f'Event {id} soft deleted.')
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to delete event: {str(e)}')
            return False
