from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Companies import CompaniesModel
import logging
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload

logger = logging.getLogger('Models.Companies.RetrieveCompanies')

class RetrieveCompanies(BaseCRUD):
    """
    Class to handle retrieving records from the companies table.
    """
    def __init__(self, session):
        super().__init__(session, CompaniesModel)

    def get_by_event(self, event_id):
        """
        Retrieve companies by event.
        """
        event_id = validate_uuid(event_id, 'event_id')
        logger.info(f'Retrieving companies for event {event_id}')
        return self.session.query(CompaniesModel).filter(
            CompaniesModel.event_id == event_id).all()

    def get_by_zone(self, zone_id):
        """
        Retrieve companies by zone.
        """
        zone_id = validate_uuid(zone_id, 'zone_id')
        logger.info(f'Retrieving companies for zone {zone_id}')
        return self.session.query(CompaniesModel).filter(
            CompaniesModel.zone_id == zone_id,
        ).all()

    def search_by_name(self, event_id, name_query):
        """
        Search companies by name in event.
        """
        event_id = validate_uuid(event_id, 'event_id')
        name_query = validate_string(name_query, 'name_query')
        logger.info(f'Searching companies "{name_query}" in event {event_id}')
        return self.session.query(CompaniesModel).filter(
            CompaniesModel.event_id == event_id,
            CompaniesModel.name.ilike(f'%{name_query}%')).all()

    def get_paginated_by_zone(self, zone_id, search=None, page=1, limit=20):
        '''Paginated companies by zone with optional search.'''
        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(CompaniesModel).options(
            joinedload(CompaniesModel.zone),
            joinedload(CompaniesModel.event)
        ).filter(
            CompaniesModel.zone_id == zone_id)

        if search:
            query = query.filter(CompaniesModel.name.ilike(f"%{search}%"))

        total = query.count()

        query = query.order_by(CompaniesModel.created_at.desc()).offset((page - 1) * limit).limit(limit)

        companies = query.all()

        company_list = []
        for company in companies:
            zone_name = company.zone.name if company.zone else None
            event_name = company.event.title if company.event else None
            company_dict = {
                "id": str(company.id),
                "name": company.name,
                "booth_number": company.booth_number,
                "slug": company.slug,
                "logo_url": company.logo_url,
                "description": company.description,
                "website": company.website,
                "industry": company.industry,
                "email": company.email,
                "phone": company.phone,
                "zone_id": str(company.zone_id),
                "zone_name": zone_name,
                "event_id": str(company.event_id),
                "event_name": event_name,
                "created_at": company.created_at.isoformat() if company.created_at else None
            }
            company_list.append(company_dict)

        return {"data": company_list, "total": total, "page": page, "limit": limit}

    def list_paginated(self, search=None, event_id=None, zone_id=None, booth_number=None, page=1, limit=20):
        '''Paginated companies with filters.'''
        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(CompaniesModel)
        if event_id:
            event_id = validate_uuid(event_id, "event_id")
            query = query.filter(CompaniesModel.event_id == event_id)

        if zone_id:
            zone_id = validate_uuid(zone_id, "zone_id")
            query = query.filter(CompaniesModel.zone_id == zone_id)

        if search:
            query = query.filter(CompaniesModel.name.ilike(f"%{search}%"))

        if booth_number:
            query = query.filter(CompaniesModel.booth_number.ilike(f"%{booth_number}%"))

        total = query.count()

        query = query.options(
            joinedload(CompaniesModel.zone),
            joinedload(CompaniesModel.event)
        ).order_by(CompaniesModel.created_at.desc()).offset((page - 1) * limit).limit(limit)

        companies = query.all()

        company_list = []
        for company in companies:
            zone_name = company.zone.name if company.zone else None
            event_name = company.event.title if company.event else None
            company_dict = {
                "id": str(company.id),
                "name": company.name,
                "booth_number": company.booth_number,
                "slug": company.slug,
                "logo_url": company.logo_url,
                "description": company.description,
                "website": company.website,
                "industry": company.industry,
                "email": company.email,
                "phone": company.phone,
                "zone_id": str(company.zone_id) if company.zone_id else None,
                "zone_name": zone_name,
                "event_id": str(company.event_id),
                "event_name": event_name,
                "created_at": company.created_at.isoformat() if company.created_at else None
            }
            company_list.append(company_dict)

        return {"data": company_list, "total": total, "page": page, "limit": limit}
