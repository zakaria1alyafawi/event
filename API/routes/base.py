from flask import Blueprint, g
from Models.Configuration import Configuration
from Models.Session import DatabaseSession
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger("api.routes.base")

class BaseRoute:
    """
    Base class for API routes, providing common functionality and session management.
    """
    def __init__(self):
        self.config = Configuration(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        self.db_session = DatabaseSession(self.config)
        self.db_session.create_database_if_not_exists()
        self.bp = Blueprint(self.__class__.__name__.lower(), __name__)
        self.register_routes()

    def get_session(self):
        """
        Create a new SQLAlchemy session for the current request.
        """
        session = self.db_session.get_session()
        session.expire_on_commit = False
        g.sessions = getattr(g, 'sessions', [])
        g.sessions.append(session)
        logger.debug("Created new SQLAlchemy session for request")
        return session

    def register_routes(self):
        """To be implemented by subclasses to define routes."""
        pass