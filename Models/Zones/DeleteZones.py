from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .Zones import ZonesModel
import logging
from datetime import datetime

logger = logging.getLogger('Models.Zones.DeleteZones')

class DeleteZones(BaseCRUD):
    """
    Class to handle soft deleting records from the zones table.
    """
    def __init__(self, session):
        super().__init__(session, ZonesModel)

    def delete(self, id):
        """
        Soft delete a ZonesModel record by ID.
        """
        id = validate_uuid(id, 'id')
        zone = self.session.query(ZonesModel).filter(ZonesModel.id == id).first()
        if not zone:
            logger.warning(f'Zone {id} not found.')
            return False
        zone.deleted_at = datetime.utcnow()
        try:
            self.session.commit()
            logger.info(f'Zone {id} soft deleted.')
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to delete zone: {str(e)}')
            return False
