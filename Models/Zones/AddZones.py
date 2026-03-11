from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string, validate_integer, validate_bool
from .Zones import ZonesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.Zones.AddZones')

class AddZones(BaseCRUD):
    """
    Class to handle adding new records to the zones table.
    """
    def __init__(self, session):
        super().__init__(session, ZonesModel)

    def add(self, event_id, name, code, capacity=None, is_restricted=False, location_x=None, location_y=None):
        """
        Add a new ZonesModel record.
        """
        event_id = validate_uuid(event_id, 'event_id')
        name = validate_string(name, 'name', max_length=200)
        code = validate_string(code, 'code', max_length=50)
        if capacity is not None:
            capacity = validate_integer(capacity, 'capacity')
        is_restricted = validate_bool(is_restricted, 'is_restricted')
        if location_x is not None:
            location_x = validate_integer(location_x, 'location_x')
        if location_y is not None:
            location_y = validate_integer(location_y, 'location_y')

        logger.info(f'Adding zone {code} to event {event_id}...')
        new_record = ZonesModel(
            event_id=event_id,
            name=name,
            code=code,
            capacity=capacity,
            is_restricted=is_restricted,
            location_x=location_x,
            location_y=location_y
        )
        self.session.add(new_record)
        try:
            self.commit()
            logger.info('Zone added successfully.')
            return new_record
        except IntegrityError as e:
            self.session.rollback()
            if 'uq_zones_event_code' in str(e):
                raise ValueError(f'Zone code "{code}" already exists for event {event_id}.')
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to add zone: {str(e)}')
            raise
