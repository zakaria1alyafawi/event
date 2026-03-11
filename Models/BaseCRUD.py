import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from Models.Utility import handle_errors
# from API.utils.encryption import PasswordHasher

logger = logging.getLogger('Models.BaseCRUD')

class BaseCRUD:
    '''
    Enhanced Base class for common CRUD operations.
    Supports auto password hashing, soft delete, active filtering, validation hooks.
    '''
    def __init__(self, session: Session, model_class):
        if not isinstance(session, Session):
            raise TypeError('Expected a valid SQLAlchemy Session object.')
        self.session = session
        self.model_class = model_class

    def _hash_password_if_present(self, kwargs):
        '''Auto hash password if present in kwargs.'''
        if 'Password' in kwargs:
            from API.utils.encryption import PasswordHasher
            kwargs['Password'] = PasswordHasher.hash_password(kwargs['Password'])
            logger.debug('Password hashed before save.')

    def _soft_delete(self, record_id):
        '''Soft delete by setting Status=3 if model has Status field.'''
        if hasattr(self.model_class, 'Status'):
            return self.update(record_id, Status=3)  # DELETED
        return False

    def commit_transaction(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.session.commit()
                logger.info('Transaction committed successfully.')
                return result
            except SQLAlchemyError as e:
                self.session.rollback()
                logger.error(f'Transaction failed and rolled back: {e}')
                raise
        return wrapper

    @commit_transaction
    def add(self, **kwargs):
        self._hash_password_if_present(kwargs)
        new_record = self.model_class(**kwargs)
        self.session.add(new_record)
        logger.info(f'Added new {self.model_class.__name__}: {new_record}')
        return new_record

    def get_all(self):
        records = self.session.query(self.model_class).all()
        logger.info(f'Retrieved {len(records)} {self.model_class.__name__} records.')
        return records

    def list(self, active_only=True, **filters):
        '''List records, filter active by default, optional filters.'''
        query = self.session.query(self.model_class)
        if active_only and hasattr(self.model_class, 'Status'):
            query = query.filter(self.model_class.Status != 3)  # exclude DELETED
        if filters:
            query = query.filter_by(**filters)
        records = query.all()
        logger.info(f'Listed {len(records)} {self.model_class.__name__} (active_only={active_only}).')
        return records

    def get_by_id(self, record_id):
        primary_key_column = self.model_class.__mapper__.primary_key[0].name
        record = self.session.query(self.model_class).filter_by(**{primary_key_column: record_id}).first()
        if record:
            logger.info(f'Retrieved {self.model_class.__name__} ID={record_id}.')
        return record

    @commit_transaction
    def update(self, record_id, **kwargs):
        record = self.get_by_id(record_id)
        if not record:
            logger.warning(f'No {self.model_class.__name__} ID={record_id}.')
            return None
        self._hash_password_if_present(kwargs)
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
        logger.info(f'Updated {self.model_class.__name__} ID={record_id}.')
        return record

    @commit_transaction
    def delete(self, record_id):
        '''Soft or hard delete based on model.'''
        if self._soft_delete(record_id):
            logger.info(f'Soft deleted {self.model_class.__name__} ID={record_id}.')
            return True
        record = self.get_by_id(record_id)
        if not record:
            logger.warning(f'No {self.model_class.__name__} ID={record_id}.')
            return False
        self.session.delete(record)
        logger.info(f'Hard deleted {self.model_class.__name__} ID={record_id}.')
        return True

    @handle_errors
    def commit(self):
        self.session.commit()
        logger.info('Manual commit successful.')
