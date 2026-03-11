from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_string, validate_uuid, validate_date, validate_bool
from .Events import EventsModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.Events.AddEvents')

class AddEvents(BaseCRUD):
    """
    Class to handle adding new records to the events table.
    """
    def __init__(self, session):
        super().__init__(session, EventsModel)

    def add(self, slug, title, start_date, end_date, venue=None, description=None, organizer_id=None, is_published=False):
        """
        Add a new EventsModel record.
        """
        slug = validate_string(slug, 'slug', max_length=100)
        title = validate_string(title, 'title', max_length=500)
        start_date = validate_date(start_date, 'start_date')
        end_date = validate_date(end_date, 'end_date')
        if start_date > end_date:
            raise ValueError('start_date must be before end_date')
        if venue:
            venue = validate_string(venue, 'venue', max_length=200)
        if description:
            description = validate_string(description, 'description', max_length=2000)
        if organizer_id:
            organizer_id = validate_uuid(organizer_id, 'organizer_id')
        is_published = validate_bool(is_published, 'is_published')

        logger.info(f'Adding event {slug}...')
        new_record = EventsModel(
            slug=slug,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            venue=venue,
            organizer_id=organizer_id,
            is_published=is_published
        )
        self.session.add(new_record)
        try:
            self.commit()
            logger.info('Event added successfully.')
            return new_record
        except IntegrityError as e:
            self.session.rollback()
            if 'uq_events_slug' in str(e):  # assume constraint
                raise ValueError(f'Slug "{slug}" already exists.')
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to add event: {str(e)}')
            raise
