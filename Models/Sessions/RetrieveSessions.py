from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .UserSessions import Session
import logging

logger = logging.getLogger('Models.Sessions.RetrieveSessions')

class RetrieveSessions(BaseCRUD):
    """
    Class to handle retrieving records from the Sessions table.
    """
    def __init__(self, session):
        super().__init__(session, Session)

    def get_by_user_id(self, user_id):
        """
        Retrieve Session records by UserID.
        """
        user_id = validate_uuid(user_id, "user_id")
        logger.info(f"Retrieving Sessions records with UserID={user_id}...")
        records = self.session.query(Session).filter(Session.UserID == user_id).all()
        logger.info(f"Retrieved {len(records)} record(s) with UserID={user_id}.")
        return records

    def get_by_token(self, token):
        """
        Retrieve Session records by Token.
        """
        token = validate_string(token, "token", max_length=500)
        logger.info(f"Retrieving Sessions records with token={token}...")
        records = self.session.query(Session).filter(Session.Token == token).all()
        logger.info(f"Retrieved {len(records)} record(s) with token={token}.")
        return records
