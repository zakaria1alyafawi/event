import logging
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, String, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Users.Users import UserModel
from Models.Base import Base

# Set up logging
logger = logging.getLogger('Models.Sessions')

class Session(Base):
    """
    SQLAlchemy model for the Sessions table.
    Represents sessions associated with a user.
    """
    __tablename__ = 'Sessions'
    __table_args__ = (
        Index('idx_sessions_user_id', 'UserID'),
        Index('idx_sessions_status', 'Status'),
        Index('idx_sessions_start_time', 'StartTime'),
        Index('idx_sessions_created_at', 'Created_at'),
    )
    SessionID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    StartTime = Column(TIMESTAMP(timezone=True), nullable=False)
    EndTime = Column(TIMESTAMP(timezone=True), nullable=True)
    Token  = Column(String(500), nullable=False)
    Status = Column(Integer, nullable=False)
    Created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    # Relationship
    user = relationship("UserModel", back_populates="sessions")

    def __init__(self, UserID, StartTime, EndTime, Token, Status, Created_at):
        self.UserID = UserID
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Token = Token
        self.Status = Status
        self.Created_at = Created_at

    def __repr__(self):
        return f'<Session(SessionID={self.SessionID}, UserID={self.UserID}, Token={self.Token[:20]}..., Status={self.Status})>'
