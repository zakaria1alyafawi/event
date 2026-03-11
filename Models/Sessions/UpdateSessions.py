from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string, validate_integer
from .UserSessions import Session
import logging

logger = logging.getLogger('Models.Sessions.UpdateSessions')

class UpdateSessions(BaseCRUD):
    """
    Class to handle updating records in the Sessions table.
    """
    def __init__(self, session):
        super().__init__(session, Session)

    def update(self, SessionID, **kwargs):
        """
        Update a Session record by ID.
        """
        if 'UserID' in kwargs:
            kwargs['UserID'] = validate_uuid(kwargs['UserID'], "UserID", optional=True)
        if 'Token' in kwargs:
            kwargs['Token'] = validate_string(kwargs['Token'], "Token", max_length=500)
        if 'Status' in kwargs:
            kwargs['Status'] = validate_integer(kwargs['Status'], "Status")

        logger.info(f"Updating Session record with SessionID={SessionID}...")
        updated_record = super().update(record_id=SessionID, **kwargs)
        if updated_record:
            logger.info(f"Record with SessionID={SessionID} updated successfully.")
        return updated_record
