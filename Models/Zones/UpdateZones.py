from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string, validate_integer, validate_bool
from .Zones import ZonesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.Zones.UpdateZones')

class UpdateZones(BaseCRUD):
    """
    Class to handle updating records in the zones table.
    """
    def __init__(self, session):
        super().__init__(session, ZonesModel)

    def update(self, id, **kwargs):
        """
        Update a ZonesModel record by ID.
        """
        id = validate_uuid(id, 'id')

        if 'event_id' in kwargs:
            kwargs['event_id'] = validate_uuid(kwargs['event_id'], 'event_id')
        if 'name' in kwargs:
            kwargs['name'] = validate_string(kwargs['name'], 'name', max_length=200)
        if 'code' in kwargs:
            kwargs['code'] = validate_string(kwargs['code'], 'code', max_length=50)
        if 'capacity' in kwargs:
            kwargs['capacity'] = validate_integer(kwargs['capacity'], 'capacity')
        if 'is_restricted' in kwargs:
            kwargs['is_restricted'] = validate_bool(kwargs['is_restricted'], 'is_restricted')
        if 'location_x' in kwargs:
            kwargs['location_x'] = validate_integer(kwargs['location_x'], 'location_x')
        if 'location_y' in kwargs:
            kwargs['location_y'] = validate_integer(kwargs['location_y'], 'location_y')

        logger.info(f'Updating zone {id}...')
        try:
            updated_record = super().update(record_id=id, **kwargs)
            if updated_record:
                logger.info(f'Zone {id} updated.')
            return updated_record
        except IntegrityError as e:
            self.session.rollback()
            if 'uq_zones_event_code' in str(e):
                raise ValueError('Zone code conflict.')
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to update zone: {str(e)}')
            raise
