import logging
from sqlalchemy import Column, DateTime, Index, ForeignKey, func, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Base import Base
from Models.Users.Users import UserModel
from Models.UserTypes.UserTypes import UserTypesModel
# Events later

logger = logging.getLogger('Models.UserRoles')

class UserRolesModel(Base):
    """
    SQLAlchemy model for the user_roles junction table.
    """
    __tablename__ = 'user_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey('user_types.id', ondelete='RESTRICT'), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('uq_user_roles_global', 'user_id', 'role_id', unique=True, postgresql_where=text('event_id IS NULL')),
        Index('uq_user_roles_event', 'user_id', 'role_id', 'event_id', unique=True, postgresql_where=text('event_id IS NOT NULL')),
        Index('idx_user_roles_user_event', 'user_id', 'event_id'),
    )

    # Relationships
    user = relationship('UserModel', back_populates='user_roles')
    role = relationship('UserTypesModel', back_populates='user_roles')
    # event = relationship('EventsModel', back_populates='user_roles')

    def __repr__(self):
        return f'<UserRoles(id={self.id}, user_id={self.user_id}, role_id={self.role_id}, event_id={self.event_id})>'
