import logging
from sqlalchemy import Column, Text, DateTime, UniqueConstraint, text, func
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from Models.Base import Base

# Set up logging
logger = logging.getLogger('Models.UserTypes')

class UserTypesModel(Base):
    """
    SQLAlchemy model for the user_types table.
    """
    __tablename__ = 'user_types'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(ENUM('super_admin', 'event_admin', 'security', 'exhibitor_staff', 'visitor', name='user_role', create_constraint=False), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uq_user_types_name'),
    )

    # Relationships (to be extended)
    user_roles = relationship("UserRolesModel", back_populates="role")

    def __repr__(self):
        return f"<UserTypes(id={self.id}, name={self.name}, description={self.description})>"
