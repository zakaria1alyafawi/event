from Models.BaseCRUD import BaseCRUD
from Models.Utility import validate_uuid
from .Connections import ConnectionsModel
import logging
from sqlalchemy.orm import joinedload
from Models.Users.Users import UserModel

logger = logging.getLogger('Models.Connections.RetrieveConnections')

class RetrieveConnections(BaseCRUD):
    """
    Class to handle retrieving records from the connections table.
    """
    def __init__(self, session):
        super().__init__(session, ConnectionsModel)

    def get_connections_for_user(self, user_id, event_id=None):
        """
        Get connections for a user (event-specific or global).
        """
        user_id = validate_uuid(user_id, 'user_id')
        query = self.session.query(ConnectionsModel).filter(ConnectionsModel.user_id == user_id)
        if event_id:
            event_id = validate_uuid(event_id, 'event_id')
            query = query.filter(ConnectionsModel.event_id == event_id)
        else:
            query = query.filter(ConnectionsModel.event_id.is_(None))
        logger.info(f'Retrieving connections for user {user_id}')
        return query.order_by(ConnectionsModel.scanned_at.desc()).all()

    def list_paginated(self, user_id, page=1, limit=20):
        '''Paginated connections for user.'''
        page = max(1, page)
        limit = min(100, max(1, limit))
        query = self.session.query(ConnectionsModel).options(
            joinedload(ConnectionsModel.connected_to).joinedload(UserModel.company)
        ).filter(ConnectionsModel.user_id == user_id)

        total = query.count()

        query = query.order_by(ConnectionsModel.scanned_at.desc()).offset((page - 1) * limit).limit(limit)

        connections = query.all()

        connection_list = []
        for conn in connections:
            conn_user = conn.connected_to
            connection_list.append({
                "email": conn_user.email,
                "phone": conn_user.phone,
                "first_name": conn_user.first_name,
                "last_name": conn_user.last_name,
                "display_name": conn_user.display_name,
                "job_title": conn_user.job_title,
                "photo_url": conn_user.photo_url,
                "company_name": conn_user.company.name if conn_user.company else None
            })

        return {"data": connection_list, "total": total, "page": page, "limit": limit}
