from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_integer
from .UserSessions import Session
import logging

logger = logging.getLogger('Models.Sessions.DeleteSessions')

class DeleteSessions(BaseCRUD):
    """
    Class to handle deleting records from the Sessions table.
    """
    def __init__(self, session):
        super().__init__(session, Session)

    def delete(self, SessionID):
        """
        Delete a Session record by ID.
        """
        SessionID = validate_integer(SessionID, "SessionID")
        logger.info(f"Deleting Session record with SessionID={SessionID}...")
        success = super().delete(record_id=SessionID)
        if success:
            logger.info(f"Record with SessionID={SessionID} deleted successfully.")
        return success
