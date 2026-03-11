from flask import Blueprint
from sqlalchemy import inspect
from API.utils.db_config import get_db_config
from Models.Session import DatabaseSession
import logging

logger = logging.getLogger('API.routes.health')

class HealthRoute:
    bp = Blueprint('health', __name__, url_prefix='/health')

    @bp.route('/', methods=['GET'])
    def health():
        try:
            config = get_db_config()
            db_session = DatabaseSession(config)
            inspector = inspect(db_session.engine)
            tables = inspector.get_table_names()
            db_session.engine.dispose()
            logger.info(f'Health check OK, {len(tables)} tables')
            return {
                'status': 'healthy',
                'db_connected': True,
                'table_count': len(tables)
            }, 200
        except Exception as e:
            logger.error(f'Health check failed: {e}')
            return {
                'status': 'unhealthy',
                'db_connected': False,
                'error': str(e)
            }, 500