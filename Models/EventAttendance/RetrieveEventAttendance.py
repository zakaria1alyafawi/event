from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .EventAttendance import EventAttendanceModel
from sqlalchemy import func
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('Models.EventAttendance.RetrieveEventAttendance')

class RetrieveEventAttendance(BaseCRUD):
    """
    Class to handle retrieving records from the event_attendance table.
    """
    def __init__(self, session):
        super().__init__(session, EventAttendanceModel)

    def get_attendance(self, event_id, user_id=None):
        """
        Get attendance for event (optional user).
        """
        event_id = validate_uuid(event_id, 'event_id')
        query = self.session.query(EventAttendanceModel).filter(EventAttendanceModel.event_id == event_id)
        if user_id:
            user_id = validate_uuid(user_id, 'user_id')
            query = query.filter(EventAttendanceModel.user_id == user_id)
        logger.info(f'Retrieving attendance for event {event_id}')
        return query.order_by(EventAttendanceModel.scanned_at.desc()).all()

    def get_user_attendance(self, user_id, event_id=None):
        """
        Get user's attendance for event or all.
        """
        user_id = validate_uuid(user_id, 'user_id')
        query = self.session.query(EventAttendanceModel).filter(EventAttendanceModel.user_id == user_id)
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')
            query = query.filter(EventAttendanceModel.event_id == event_id)
        logger.info(f'Retrieving attendance for user {user_id}')
        return query.order_by(EventAttendanceModel.scanned_at.desc()).all()

    def get_event_stats(self, event_id):
        """
        Get scan stats for event.
        """
        event_id = validate_uuid(event_id, 'event_id')
        stats = self.session.query(
            EventAttendanceModel.action,
            func.count().label('count')
        ).filter(EventAttendanceModel.event_id == event_id).group_by(EventAttendanceModel.action).all()
        logger.info(f'Event {event_id} stats: {stats}')
        return dict(stats)

    def get_last_attendance(self, user_id, event_id):
        '''Last attendance for user in event.'''
        user_id = validate_uuid(user_id, 'user_id')
        event_id = validate_uuid(event_id, 'event_id')
        return self.session.query(EventAttendanceModel).filter(
            EventAttendanceModel.user_id == user_id,
            EventAttendanceModel.event_id == event_id
        ).order_by(EventAttendanceModel.scanned_at.desc()).first()

    def get_last_attendance(self, user_id, event_id):
        '''Last attendance for user in event desc.'''
        user_id = validate_uuid(user_id, 'user_id')
        event_id = validate_uuid(event_id, 'event_id')
        return self.session.query(EventAttendanceModel).filter(
            EventAttendanceModel.user_id == user_id,
            EventAttendanceModel.event_id == event_id
        ).order_by(EventAttendanceModel.scanned_at.desc()).first()

    def get_daily_counts(self, days=7):
        """
        Get daily attendance counts for the last `days` days, including zeros.
        """
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days - 1)
        query = self.session.query(
            func.date(EventAttendanceModel.scanned_at).label("date"),
            func.count().label("count")
        ).filter(
            EventAttendanceModel.scanned_at >= start_dt
        ).group_by(func.date(EventAttendanceModel.scanned_at)).order_by(func.date(EventAttendanceModel.scanned_at).desc()).all()
        results = {row.date: int(row.count) for row in query}
        dates = []
        current_date = end_dt.date()
        for i in range(days):
            date_obj = current_date - timedelta(days=i)
            dates.append(date_obj)
        return [{"date": d.strftime("%Y-%m-%d"), "count": results.get(d, 0)} for d in dates]
