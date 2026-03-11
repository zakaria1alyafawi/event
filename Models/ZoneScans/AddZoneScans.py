from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_enum, validate_bool, validate_string
from .ZoneScans import ZoneScansModel
import logging
from datetime import datetime

logger = logging.getLogger('Models.ZoneScans.AddZoneScans')

class AddZoneScans(BaseCRUD):
    """
    Class to handle adding new records to the zone_scans table.
    """
    def __init__(self, session):
        super().__init__(session, ZoneScansModel)

    def record_scan(self, user_id, zone_id, action, scanner_id=None, is_valid=True, denial_reason=None, device_info=None):
        """
        Record a zone scan.
        """
        user_id = validate_uuid(user_id, 'user_id')
        zone_id = validate_uuid(zone_id, 'zone_id')
        scan_actions = ['enter', 'exit']
        action = validate_enum(action, 'action', scan_actions)
        if scanner_id:
            scanner_id = validate_uuid(scanner_id, 'scanner_id')
        is_valid = validate_bool(is_valid, 'is_valid')
        if denial_reason:
            denial_reason = validate_string(denial_reason, 'denial_reason', max_length=500)

        logger.info(f'Recording zone scan for user {user_id} zone {zone_id} action {action}')
        new_record = ZoneScansModel(
            user_id=user_id,
            zone_id=zone_id,
            scanner_id=scanner_id,
            action=action,
            scanned_at=datetime.utcnow(),
            is_valid=is_valid,
            denial_reason=denial_reason,
            device_info=device_info
        )
        self.session.add(new_record)
        self.commit()
        logger.info('Zone scan recorded.')
        return new_record
