import logging
from sqlalchemy import Column, DateTime, Text, UniqueConstraint, Index, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Users.Users import UserModel
from Models.Events.Events import EventsModel

logger = logging.getLogger('Models.Connections')

class ConnectionsModel(Base):
    """
    SQLAlchemy model for the connections table.
    """
    __tablename__ = 'connections'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    connected_to_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='SET NULL'), nullable=True)
    scanned_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'connected_to_id', 'event_id', name='uq_connections_pair_event'),
        Index('idx_connections_user_event', 'user_id', 'event_id'),
    )

    # Relationships
    user = relationship('UserModel', foreign_keys=[user_id])
    connected_to = relationship('UserModel', foreign_keys=[connected_to_id])
    event = relationship('EventsModel')

    def __repr__(self):
        return f'<Connection(id={self.id}, user_id={self.user_id}, connected_to_id={self.connected_to_id}, event_id={self.event_id})>'
