import logging
from sqlalchemy import Column, DateTime, Text, Boolean, Index, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Users.Users import UserModel
from Models.Zones.Zones import ZonesModel

logger = logging.getLogger('Models.ZoneScans')

class ZoneScansModel(Base):
    """
    SQLAlchemy model for the zone_scans table.
    """
    __tablename__ = 'zone_scans'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    zone_id = Column(UUID(as_uuid=True), ForeignKey('zones.id'), nullable=False, index=True)
    scanner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    action = Column(ENUM('enter', 'exit', name='scan_action', create_constraint=False), nullable=False)
    scanned_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_valid = Column(Boolean, default=True, server_default=text('true'))
    denial_reason = Column(Text)
    device_info = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_zone_scans_zone_time', 'zone_id', 'scanned_at'),
        Index('idx_zone_scans_user_zone', 'user_id', 'zone_id'),
    )

    # Relationships
    user = relationship('UserModel', foreign_keys=[user_id])
    zone = relationship('ZonesModel')
    scanner = relationship('UserModel', foreign_keys=[scanner_id])

    def __repr__(self):
        return f'<ZoneScan(id={self.id}, user_id={self.user_id}, zone_id={self.zone_id}, action={self.action})>'
