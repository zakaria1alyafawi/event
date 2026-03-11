from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_enum, validate_bool, validate_string
from .EventAttendance import EventAttendanceModel
import logging
from datetime import datetime

logger = logging.getLogger('Models.EventAttendance.AddEventAttendance')

class AddEventAttendance(BaseCRUD):
    """
    Class to handle adding new records to the event_attendance table.
    """
    def __init__(self, session):
        super().__init__(session, EventAttendanceModel)

    def record_scan(self, user_id, event_id, action, scanner_id=None, is_valid=True, denial_reason=None, device_info=None):
        """
        Record an event attendance scan.
        """
        user_id = validate_uuid(user_id, 'user_id')
        event_id = validate_uuid(event_id, 'event_id')
        scan_actions = ['enter', 'exit']
        action = validate_enum(action, 'action', scan_actions)
        if scanner_id:
            scanner_id = validate_uuid(scanner_id, 'scanner_id')
        is_valid = validate_bool(is_valid, 'is_valid')
        if denial_reason:
            denial_reason = validate_string(denial_reason, 'denial_reason', max_length=500)
        # device_info dict assumed valid JSONB serializable

        logger.info(f'Recording scan for user {user_id} event {event_id} action {action}')
        new_record = EventAttendanceModel(
            user_id=user_id,
            event_id=event_id,
            scanner_id=scanner_id,
            action=action,
            scanned_at=datetime.utcnow(),
            is_valid=is_valid,
            denial_reason=denial_reason,
            device_info=device_info
        )
        self.session.add(new_record)
        self.commit()
        logger.info('Scan recorded.')
        return new_record
