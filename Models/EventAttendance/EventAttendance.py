import logging
from sqlalchemy import Column, DateTime, Text, Boolean, Index, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Users.Users import UserModel
from Models.Events.Events import EventsModel

logger = logging.getLogger('Models.EventAttendance')

class EventAttendanceModel(Base):
    """
    SQLAlchemy model for the event_attendance table.
    """
    __tablename__ = 'event_attendance'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), nullable=False, index=True)
    scanner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    action = Column(ENUM('enter', 'exit', name='scan_action', create_constraint=False), nullable=False)
    scanned_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_valid = Column(Boolean, default=True, server_default=text('true'))
    denial_reason = Column(Text)
    device_info = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_event_attendance_user_event', 'user_id', 'event_id'),
        Index('idx_event_attendance_event_time', 'event_id', 'scanned_at'),
    )

    # Relationships
    user = relationship('UserModel', foreign_keys=[user_id])
    event = relationship('EventsModel')
    scanner = relationship('UserModel', foreign_keys=[scanner_id])

    def __repr__(self):
        return f'<EventAttendance(id={self.id}, user_id={self.user_id}, event_id={self.event_id}, action={self.action})>'
