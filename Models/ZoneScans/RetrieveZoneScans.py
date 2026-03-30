from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .ZoneScans import ZoneScansModel
from sqlalchemy import func
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('Models.ZoneScans.RetrieveZoneScans')

class RetrieveZoneScans(BaseCRUD):
    """
    Class to handle retrieving records from the zone_scans table.
    """
    def __init__(self, session):
        super().__init__(session, ZoneScansModel)

    def get_scans(self, zone_id, user_id=None):
        """
        Get scans for zone (optional user).
        """
        zone_id = validate_uuid(zone_id, 'zone_id')
        query = self.session.query(ZoneScansModel).filter(ZoneScansModel.zone_id == zone_id)
        if user_id:
            user_id = validate_uuid(user_id, 'user_id')
            query = query.filter(ZoneScansModel.user_id == user_id)
        logger.info(f'Retrieving scans for zone {zone_id}')
        return query.order_by(ZoneScansModel.scanned_at.desc()).all()

    def get_user_scans_zone(self, user_id, zone_id):
        """
        Get user's scans for zone.
        """
        user_id = validate_uuid(user_id, 'user_id')
        zone_id = validate_uuid(zone_id, 'zone_id')
        logger.info(f'Retrieving scans for user {user_id} zone {zone_id}')
        return self.session.query(ZoneScansModel).filter(
            ZoneScansModel.user_id == user_id,
            ZoneScansModel.zone_id == zone_id
        ).order_by(ZoneScansModel.scanned_at.desc()).all()

    def get_zone_stats(self, zone_id):
        """
        Get scan stats for zone.
        """
        zone_id = validate_uuid(zone_id, 'zone_id')
        stats = self.session.query(
            ZoneScansModel.action,
            func.count().label('count')
        ).filter(ZoneScansModel.zone_id == zone_id).group_by(ZoneScansModel.action).all()
        logger.info(f'Zone {zone_id} stats: {stats}')
        return dict(stats)

    def get_last_scan(self, user_id, zone_id):
        '''Last scan for user in zone.'''
        user_id = validate_uuid(user_id, 'user_id')
        zone_id = validate_uuid(zone_id, 'zone_id')
        return self.session.query(ZoneScansModel).filter(
            ZoneScansModel.user_id == user_id,
            ZoneScansModel.zone_id == zone_id
        ).order_by(ZoneScansModel.scanned_at.desc()).first()

    def get_zone_occupancy(self, zone_id):
        '''Enter - exit count.'''
        zone_id = validate_uuid(zone_id, 'zone_id')
        enter_count = self.session.query(func.count()).filter(
            ZoneScansModel.zone_id == zone_id,
            ZoneScansModel.action == 'enter'
        ).scalar()
        exit_count = self.session.query(func.count()).filter(
            ZoneScansModel.zone_id == zone_id,
            ZoneScansModel.action == 'exit'
        ).scalar()
        return enter_count - exit_count

    def get_last_scan(self, user_id, zone_id):
        '''Last scan for user in zone desc.'''
        user_id = validate_uuid(user_id, 'user_id')
        zone_id = validate_uuid(zone_id, 'zone_id')
        return self.session.query(ZoneScansModel).filter(
            ZoneScansModel.user_id == user_id,
            ZoneScansModel.zone_id == zone_id
        ).order_by(ZoneScansModel.scanned_at.desc()).first()

    def get_daily_counts(self, days=7):
        """
        Get daily scan counts for the last `days` days, including zeros.
        """
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days - 1)
        query = self.session.query(
            func.date(ZoneScansModel.scanned_at).label("date"),
            func.count().label("count")
        ).filter(
            ZoneScansModel.scanned_at >= start_dt
        ).group_by(func.date(ZoneScansModel.scanned_at)).order_by(func.date(ZoneScansModel.scanned_at).desc()).all()
        results = {row.date: int(row.count) for row in query}
        dates = []
        current_date = end_dt.date()
        for i in range(days):
            date_obj = current_date - timedelta(days=i)
            dates.append(date_obj)
        return [{"date": d.strftime("%Y-%m-%d"), "count": results.get(d, 0)} for d in dates]
