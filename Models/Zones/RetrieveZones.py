from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid, validate_string
from .Zones import ZonesModel
import logging
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

logger = logging.getLogger('Models.Zones.RetrieveZones')

class RetrieveZones(BaseCRUD):
    """
    Class to handle retrieving records from the zones table.
    """
    def __init__(self, session):
        super().__init__(session, ZonesModel)

    def get_by_event(self, event_id):
        """
        Retrieve zones by event.
        """
        event_id = validate_uuid(event_id, 'event_id')
        logger.info(f'Retrieving zones for event {event_id}')
        return self.session.query(ZonesModel).filter(
            ZonesModel.event_id == event_id,
            ZonesModel.deleted_at.is_(None)
        ).all()

    def get_by_event_code(self, event_id, code):
        """
        Retrieve zone by event and code.
        """
        event_id = validate_uuid(event_id, 'event_id')
        code = validate_string(code, 'code')
        logger.info(f'Retrieving zone {code} for event {event_id}')
        return self.session.query(ZonesModel).filter(
            ZonesModel.event_id == event_id,
            ZonesModel.code == code,
            ZonesModel.deleted_at.is_(None)
        ).first()

    def list_paginated(self, search=None, event_id=None, page=1, limit=20):
        '''Paginated list of zones with optional filters.'''
        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(ZonesModel).filter(
            ZonesModel.deleted_at.is_(None)
        )

        if event_id:
            event_id = validate_uuid(event_id, "event_id")
            query = query.filter(ZonesModel.event_id == event_id)

        if search:
            query = query.filter(
                or_(
                    ZonesModel.name.ilike(f"%{search}%"),
                    ZonesModel.code.ilike(f"%{search}%")
                )
            )

        total = query.count()

        query = query.options(
            joinedload(ZonesModel.event)
        ).order_by(ZonesModel.created_at.desc()).offset((page - 1) * limit).limit(limit)

        zones = query.all()

        zone_list = []
        for zone in zones:
            event_name = zone.event.title if zone.event else None
            zone_dict = {
                "id": str(zone.id),
                "name": zone.name,
                "code": zone.code,
                "capacity": zone.capacity,
                "is_restricted": zone.is_restricted,
                "location_x": zone.location_x,
                "location_y": zone.location_y,
                "event_id": str(zone.event_id),
                "event_name": event_name,
                "created_at": zone.created_at.isoformat() if zone.created_at else None
            }
            zone_list.append(zone_dict)

        return {"data": zone_list, "total": total, "page": page, "limit": limit}
