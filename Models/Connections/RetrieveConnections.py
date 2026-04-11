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
        '''Paginated bidirectional connections with correct company name logic.'''
        from Models.UserRoles.UserRoles import UserRolesModel
        from sqlalchemy import or_
        page = max(1, page)
        limit = min(100, max(1, limit))

        # Bidirectional filter: user_id is either scanner OR scanned
        query = self.session.query(ConnectionsModel).options(
            joinedload(ConnectionsModel.connected_to)
                .joinedload(UserModel.company),
            joinedload(ConnectionsModel.connected_to)
                .selectinload(UserModel.user_roles)
                .joinedload(UserRolesModel.role)
        ).filter(
            or_(
                ConnectionsModel.user_id == user_id,          # I scanned them
                ConnectionsModel.connected_to_id == user_id   # They scanned me
            )
        )

        total = query.count()
        
        connections = query.order_by(ConnectionsModel.scanned_at.desc()) \
                        .offset((page - 1) * limit) \
                        .limit(limit) \
                        .all()

        connection_list = []
        seen = set()   # Prevent duplicates if both directions exist

        for conn in connections:
            # Determine who is the "other" user
            if conn.user_id == user_id:
                other_user = conn.connected_to
            else:
                other_user = conn.user   # Need to load this relationship too

            if not other_user or other_user.id in seen:
                continue

            seen.add(other_user.id)

            # === Company name logic based on role ===
            roles = [ur.role.name for ur in other_user.user_roles if ur.role]

            if 'visitor' in roles:
                company_name = other_user.company_name
            elif 'exhibitor_staff' in roles:
                company_name = other_user.company.name if other_user.company else None
            else:
                company_name = other_user.company_name or (other_user.company.name if other_user.company else None)

            connection_list.append({
                "email": other_user.email,
                "phone": other_user.phone,
                "first_name": other_user.first_name,
                "last_name": other_user.last_name,
                "display_name": other_user.display_name,
                "job_title": other_user.job_title,
                "photo_url": other_user.photo_url,
                "company_name": company_name
            })

        return {
            "data": connection_list,
            "total": len(connection_list),   # Note: total may need adjustment for deduplication
            "page": page,
            "limit": limit
        }