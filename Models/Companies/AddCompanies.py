from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Companies import CompaniesModel
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger('Models.Companies.AddCompanies')

class AddCompanies(BaseCRUD):
    """
    Class to handle adding new records to the companies table.
    """
    def __init__(self, session):
        super().__init__(session, CompaniesModel)

    def add(self, event_id, name, booth_number=None, zone_id=None, slug=None, logo_url=None, description=None, website=None, industry=None, email=None, phone=None):
        """
        Add a new CompaniesModel record.
        """
        event_id = validate_uuid(event_id, 'event_id')
        name = validate_string(name, 'name', max_length=200)
        if booth_number:
            booth_number = validate_string(booth_number, 'booth_number', max_length=50)
        if zone_id:
            zone_id = validate_uuid(zone_id, 'zone_id')
        if slug:
            slug = validate_string(slug, 'slug', max_length=100)
        if logo_url:
            logo_url = validate_string(logo_url, 'logo_url', max_length=500)
        if description:
            description = validate_string(description, 'description', max_length=2000)
        if website:
            website = validate_string(website, 'website', max_length=200)
        if industry:
            industry = validate_string(industry, 'industry', max_length=100)
        if email:
            email = validate_string(email, 'email', max_length=200)
        if phone:
            phone = validate_string(phone, 'phone', max_length=50)

        logger.info(f'Adding company {name} to event {event_id}...')
        new_record = CompaniesModel(
            event_id=event_id,
            zone_id=zone_id,
            name=name,
            booth_number=booth_number,
            slug=slug,
            logo_url=logo_url,
            description=description,
            website=website,
            industry=industry,
            email=email,
            phone=phone
        )
        self.session.add(new_record)
        try:
            self.commit()
            logger.info('Company added successfully.')
            return new_record
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f'Failed to add company: {str(e)}')
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f'Failed to add company: {str(e)}')
            raise
