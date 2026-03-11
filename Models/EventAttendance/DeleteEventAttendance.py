from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .EventAttendance import EventAttendanceModel
import logging

logger = logging.getLogger('Models.EventAttendance.DeleteEventAttendance')

class DeleteEventAttendance(BaseCRUD):
    """
    Class to handle deleting records from the event_attendance table.
    """
    def __init__(self, session):
        super().__init__(session, EventAttendanceModel)

    def delete(self, id):
        """
        Delete an EventAttendance record by ID (hard delete).
        """
        id = validate_uuid(id, 'id')
        logger.info(f'Deleting attendance record {id}')
        success = super().delete(record_id=id)
        if success:
            logger.info(f'Record {id} deleted.')
        return success
