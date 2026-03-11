from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Events import EventsModel
from sqlalchemy import func, or_, exists
from sqlalchemy.orm import joinedload
from datetime import date, datetime
import logging

logger = logging.getLogger('Models.Events.RetrieveEvents')

class RetrieveEvents(BaseCRUD):
    """
    Class to handle retrieving records from the events table.
    """
    def __init__(self, session):
        super().__init__(session, EventsModel)

    def get_by_slug(self, slug):
        """
        Retrieve event by slug.
        """
        slug = validate_string(slug, 'slug')
        logger.info(f'Retrieving event by slug={slug}')
        return self.session.query(EventsModel).filter(
            EventsModel.slug == slug,
            EventsModel.deleted_at.is_(None)
        ).first()

    def get_upcoming(self, limit=10, start_from_date=None):
        """
        Retrieve upcoming events.
        """
        if start_from_date is None:
            start_from_date = date.today()
        query = self.session.query(EventsModel).filter(
            EventsModel.start_date >= start_from_date,
            EventsModel.deleted_at.is_(None)
        ).order_by(EventsModel.start_date.asc()).limit(limit)
        logger.info(f'Retrieving upcoming events from {start_from_date}')
        return query.all()

    def get_by_organizer(self, organizer_id):
        """
        Retrieve events by organizer.
        """
        organizer_id = validate_uuid(organizer_id, 'organizer_id')
        logger.info(f'Retrieving events by organizer {organizer_id}')
        return self.session.query(EventsModel).filter(
            EventsModel.organizer_id == organizer_id,
            EventsModel.deleted_at.is_(None)
        ).all()

    def list_published_active(self):
        """
        List published active events.
        """
        now = date.today()
        logger.info('Retrieving published active events')
        return self.session.query(EventsModel).filter(
            EventsModel.is_published == True,
            EventsModel.deleted_at.is_(None),
            EventsModel.start_date <= now,
            EventsModel.end_date >= now
        ).order_by(EventsModel.start_date.desc()).all()

    def list_paginated(self, search=None, organizer_id=None, published=None, page=1, limit=20):
        '''Paginated list of events with optional filters.'''

        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(EventsModel).filter(
            EventsModel.deleted_at.is_(None)
        )

        if organizer_id:
            organizer_id = validate_uuid(organizer_id, "organizer_id")
            query = query.filter(EventsModel.organizer_id == organizer_id)

        if published is not None:
            query = query.filter(EventsModel.is_published == published)

        if search:
            query = query.filter(EventsModel.title.ilike(f"%{search}%"))

        total = query.count()

        query = query.options(
            joinedload(EventsModel.organizer)
        ).order_by(EventsModel.created_at.desc()).offset((page - 1) * limit).limit(limit)

        events = query.all()

        event_list = []
        for event in events:
            organizer_name = f"{event.organizer.first_name} {event.organizer.last_name}".strip() if event.organizer else None
            event_dict = {
                "id": str(event.id),
                "slug": event.slug,
                "title": event.title,
                "description": event.description,
                "start_date": event.start_date.isoformat() if event.start_date else None,
                "end_date": event.end_date.isoformat() if event.end_date else None,
                "venue": event.venue,
                "organizer_id": str(event.organizer_id) if event.organizer_id else None,
                "organizer_name": organizer_name,
                "is_published": event.is_published,
                "created_at": event.created_at.isoformat() if event.created_at else None
            }
            event_list.append(event_dict)

        return {"data": event_list, "total": total, "page": page, "limit": limit}
