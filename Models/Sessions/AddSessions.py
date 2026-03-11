from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string, validate_integer
from .UserSessions import Session
import logging

logger = logging.getLogger('Models.Sessions.AddSessions')

class AddSessions(BaseCRUD):
    """
    Class to handle adding new records to the Sessions table.
    """
    def __init__(self, session):
        super().__init__(session, Session)

    def add(self, UserID, StartTime, EndTime, Token, Status, Created_at):
        """
        Add a new Session record.
        """
        UserID = validate_uuid(UserID, "UserID", optional=True)
        Token = validate_string(Token, "Token", max_length=500)
        Status = validate_integer(Status, "Status")  # keep int

        logger.info(f"Adding Session record with UserID={UserID}...")
        new_session = Session(
            UserID=UserID,
            StartTime=StartTime,
            EndTime=EndTime,
            Token=Token,
            Status=Status,
            Created_at=Created_at
        )
        self.session.add(new_session)
        self.commit()
        logger.info("Session added successfully.")
        return new_session
