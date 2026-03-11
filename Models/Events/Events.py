import logging
from sqlalchemy import Column, Text, Date, DateTime, Boolean, Index, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Users.Users import UserModel  # organizer
from datetime import datetime

logger = logging.getLogger('Models.Events')

class EventsModel(Base):
    """
    SQLAlchemy model for the events table.
    """
    __tablename__ = 'events'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    slug = Column(Text, nullable=False, unique=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    venue = Column(Text)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    is_published = Column(Boolean, default=False, server_default=text('false'))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_events_organizer_id', 'organizer_id'),
    )

    # Relationships
    organizer = relationship('UserModel', back_populates='organized_events')
    zones = relationship('ZonesModel', back_populates='event')
    companies = relationship('CompaniesModel', back_populates='event')

    def __repr__(self):
        return f'<Event(id={self.id}, slug={self.slug}, title={self.title[:30]}...)>'

    @property
    def is_active(self):
        now = datetime.utcnow().date()
        return self.is_published and self.start_date <= now <= self.end_date and self.deleted_at is None
