import logging
from sqlalchemy import Column, Text, DateTime, ForeignKey, Index, text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Events.Events import EventsModel
from Models.Zones.Zones import ZonesModel
from Models.Users.Users import UserModel

logger = logging.getLogger('Models.Companies')

class CompaniesModel(Base):
    """
    SQLAlchemy model for the companies table.
    """
    __tablename__ = 'companies'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), nullable=False, index=True)
    zone_id = Column(UUID(as_uuid=True), ForeignKey('zones.id', ondelete='SET NULL'), nullable=True)
    name = Column(Text, nullable=False)
    booth_number = Column(Text)
    slug = Column(Text)
    logo_url = Column(Text)
    description = Column(Text)
    website = Column(Text)
    industry = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_companies_event_zone', 'event_id', 'zone_id'),
    )

    # Relationships
    event = relationship('EventsModel', back_populates='companies')
    zone = relationship('ZonesModel', back_populates='companies')
    users = relationship('UserModel', back_populates='company')

    def __repr__(self):
        return f'<Company(id={self.id}, name={self.name}, event_id={self.event_id})>'
