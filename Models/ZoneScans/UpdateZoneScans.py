from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_bool, validate_string
from .ZoneScans import ZoneScansModel
import logging

logger = logging.getLogger('Models.ZoneScans.UpdateZoneScans')

class UpdateZoneScans(BaseCRUD):
    """
    Class to handle updating records in the zone_scans table.
    """
    def __init__(self, session):
        super().__init__(session, ZoneScansModel)

    def update_valid(self, id, is_valid, denial_reason=None):
        """
        Update scan validity.
        """
        id = validate_uuid(id, 'id')
        is_valid = validate_bool(is_valid, 'is_valid')
        if denial_reason:
            denial_reason = validate_string(denial_reason, 'denial_reason', max_length=500)

        logger.info(f'Updating zone scan {id} validity to {is_valid}')
        record = self.session.query(ZoneScansModel).filter(ZoneScansModel.id == id).first()
        if not record:
            return None
        record.is_valid = is_valid
        record.denial_reason = denial_reason
        self.session.commit()
        return record
