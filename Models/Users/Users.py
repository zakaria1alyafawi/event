import logging
from sqlalchemy import Column, String, Text, DateTime, Boolean, UniqueConstraint, Index, text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from Models.Base import Base



# Set up logging
logger = logging.getLogger('Models.Users')

class UserModel(Base):
    """
    SQLAlchemy model for the users table.
    """
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    email = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    password_hash = Column(Text, nullable=False)
    auth_provider = Column(String(50), default='email', server_default=text("'email'"), nullable=False)
    auth_id = Column(Text)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    display_name = Column(String(200))
    job_title = Column(String(200))
    photo_url = Column(Text)
    country = Column(String(100))
    city = Column(String(100))
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id', ondelete='SET NULL'), nullable=True)
    access_token = Column(UUID(as_uuid=True), unique=True, server_default=text('gen_random_uuid()'))
    token_expires_at = Column(DateTime(timezone=True), nullable=True)
    token_last_rotated_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, server_default=text('true'))
    is_blacklisted = Column(Boolean, default=False, server_default=text('false'))
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('email', name='uq_users_email'),
        UniqueConstraint('phone', name='uq_users_phone'),
        UniqueConstraint('access_token', name='uq_users_access_token'),
        Index('idx_users_email', 'email'),
        Index('idx_users_phone', 'phone'),
        Index('idx_users_access_token', 'access_token'),
        Index('idx_users_company_id', 'company_id'),
    )

    # Relationships (extend later)
    company = relationship('CompaniesModel', back_populates='users')
    sessions = relationship("Session", back_populates="user")
    organized_events = relationship("EventsModel", back_populates="organizer")
    user_roles = relationship("UserRolesModel", back_populates="user")


    def __init__(self, email=None, phone=None, password_hash=None, auth_provider='email', auth_id=None, first_name=None, last_name=None, display_name=None, job_title=None, photo_url=None, country=None, city=None, company_id=None, access_token=None, token_expires_at=None, token_last_rotated_at=None, is_active=True, is_blacklisted=False, deleted_at=None):
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        self.auth_provider = auth_provider
        self.auth_id = auth_id
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.job_title = job_title
        self.photo_url = photo_url
        self.country = country
        self.city = city
        self.company_id = company_id
        self.access_token = access_token
        self.token_expires_at = token_expires_at
        self.token_last_rotated_at = token_last_rotated_at
        self.is_active = is_active
        self.is_blacklisted = is_blacklisted
        self.deleted_at = deleted_at

    def __repr__(self):
        return f'<User(id={self.id}, email={self.email}, first_name={self.first_name}, is_active={self.is_active})>'
