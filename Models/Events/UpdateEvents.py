from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string, validate_date, validate_bool
from .Events import EventsModel
import logging

logger = logging.getLogger('Models.Events.UpdateEvents')

class UpdateEvents(BaseCRUD):
    """
    Class to handle updating records in the events table.
    """
    def __init__(self, session):
        super().__init__(session, EventsModel)

    def update(self, id, **kwargs):
        """
        Update an EventsModel record by ID.
        """
        id = validate_uuid(id, 'id')

        if 'slug' in kwargs:
            kwargs['slug'] = validate_string(kwargs['slug'], 'slug', max_length=100)
        if 'title' in kwargs:
            kwargs['title'] = validate_string(kwargs['title'], 'title', max_length=500)
        if 'description' in kwargs:
            kwargs['description'] = validate_string(kwargs['description'], 'description', max_length=2000)
        if 'start_date' in kwargs:
            kwargs['start_date'] = validate_date(kwargs['start_date'], 'start_date')
        if 'end_date' in kwargs:
            kwargs['end_date'] = validate_date(kwargs['end_date'], 'end_date')
        if 'venue' in kwargs:
            kwargs['venue'] = validate_string(kwargs['venue'], 'venue', max_length=200)
        if 'organizer_id' in kwargs:
            kwargs['organizer_id'] = validate_uuid(kwargs['organizer_id'], 'organizer_id', optional=True)
        if 'is_published' in kwargs:
            kwargs['is_published'] = validate_bool(kwargs['is_published'], 'is_published')

        logger.info(f'Updating event {id}...')
        updated_record = super().update(record_id=id, **kwargs)
        if updated_record:
            logger.info(f'Event {id} updated.')
        return updated_record

    def publish(self, id):
        """
        Publish an event.
        """
        id = validate_uuid(id, 'id')
        return self.update(id, is_published=True)
