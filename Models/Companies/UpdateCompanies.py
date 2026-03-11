from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Companies import CompaniesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.Companies.UpdateCompanies')

class UpdateCompanies(BaseCRUD):
    """
    Class to handle updating records in the companies table.
    """
    def __init__(self, session):
        super().__init__(session, CompaniesModel)

    def update(self, id, **kwargs):
        """
        Update a CompaniesModel record by ID.
        """
        id = validate_uuid(id, 'id')

        if 'event_id' in kwargs:
            kwargs['event_id'] = validate_uuid(kwargs['event_id'], 'event_id')
        if 'zone_id' in kwargs:
            kwargs['zone_id'] = validate_uuid(kwargs['zone_id'], 'zone_id', optional=True)
        if 'name' in kwargs:
            kwargs['name'] = validate_string(kwargs['name'], 'name', max_length=200)
        if 'booth_number' in kwargs:
            kwargs['booth_number'] = validate_string(kwargs['booth_number'], 'booth_number', max_length=50)
        if 'slug' in kwargs:
            kwargs['slug'] = validate_string(kwargs['slug'], 'slug', max_length=100)
        if 'logo_url' in kwargs:
            kwargs['logo_url'] = validate_string(kwargs['logo_url'], 'logo_url', max_length=500)
        if 'description' in kwargs:
            kwargs['description'] = validate_string(kwargs['description'], 'description', max_length=2000)
        if 'website' in kwargs:
            kwargs['website'] = validate_string(kwargs['website'], 'website', max_length=200)
        if 'industry' in kwargs:
            kwargs['industry'] = validate_string(kwargs['industry'], 'industry', max_length=100)
        if 'email' in kwargs:
            kwargs['email'] = validate_string(kwargs['email'], 'email', max_length=200)
        if 'phone' in kwargs:
            kwargs['phone'] = validate_string(kwargs['phone'], 'phone', max_length=50)

        logger.info(f'Updating company {id}...')
        try:
            updated_record = super().update(record_id=id, **kwargs)
            if updated_record:
                logger.info(f'Company {id} updated.')
            return updated_record
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f'Update conflict: {str(e)}')
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to update company: {str(e)}')
            raise
