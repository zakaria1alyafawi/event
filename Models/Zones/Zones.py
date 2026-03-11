import logging
from sqlalchemy import Column, Text, Integer, DateTime, Boolean, UniqueConstraint, Index, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Events.Events import EventsModel

logger = logging.getLogger('Models.Zones')

class ZonesModel(Base):
    """
    SQLAlchemy model for the zones table.
    """
    __tablename__ = 'zones'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    capacity = Column(Integer)
    is_restricted = Column(Boolean, default=False, server_default=text('false'))
    location_x = Column(Integer)
    location_y = Column(Integer)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('event_id', 'code', name='uq_zones_event_code'),
        Index('idx_zones_event_code', 'event_id', 'code'),
    )

    # Relationships
    event = relationship('EventsModel', back_populates='zones')
    companies = relationship('CompaniesModel', back_populates='zone')

    def __repr__(self):
        return f'<Zone(id={self.id}, event_id={self.event_id}, name={self.name}, code={self.code})>'
