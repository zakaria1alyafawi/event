from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .ZoneScans import ZoneScansModel
import logging

logger = logging.getLogger('Models.ZoneScans.DeleteZoneScans')

class DeleteZoneScans(BaseCRUD):
    """
    Class to handle deleting records from the zone_scans table.
    """
    def __init__(self, session):
        super().__init__(session, ZoneScansModel)

    def delete(self, id):
        """
        Delete a ZoneScans record by ID (hard delete).
        """
        id = validate_uuid(id, 'id')
        logger.info(f'Deleting zone scan {id}')
        success = super().delete(record_id=id)
        if success:
            logger.info(f'Record {id} deleted.')
        return success
