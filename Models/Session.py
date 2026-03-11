import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .Configuration import Configuration

# Set up logging
logger = logging.getLogger("Models.Session")

class DatabaseSession:
    '''
    A class to manage database sessions and connections.
    Attributes:
        engine (Engine): SQLAlchemy engine for the database.
        Session (sessionmaker): SQLAlchemy sessionmaker for creating sessions.
    Methods:
        get_session(): Creates and returns a new database session.
        create_database_if_not_exists(): Checks and creates the database if it doesn't exist.
        tables_exist(): Checks if tables exist in the database.
    '''
    def __init__(self, config):
        '''
        Initializes the DatabaseSession with a Configuration object.
        Args:
            config (Configuration): A Configuration object containing database credentials.
        Raises:
            TypeError: If the provided config is not a Configuration instance.
            RuntimeError: If the database engine initialization fails.
        '''
        logger.info(f"Initializing {self.__class__.__name__}...")
        try:
            if not isinstance(config, Configuration):
                raise TypeError("Expected a Configuration instance.")

            db_url = config.get_database_url()

            self.engine = create_engine(
                db_url,
                echo=False,
                
                # ────────────────────────────────────────────────────────────────
                # FIXES FOR "server closed the connection unexpectedly"
                pool_pre_ping=True,             # ← MOST IMPORTANT: verifies connection before use
                pool_recycle=300,               # ← Recycles connections every 5 minutes
                # ────────────────────────────────────────────────────────────────
                
                # Recommended production pool settings
                pool_size=5,                    # number of persistent connections kept open
                max_overflow=10,                # additional connections allowed during peak load
                pool_timeout=30,                # seconds to wait for a connection from pool
            )
            
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Database engine and session factory initialized successfully.")
            
            # Optional: test connection right after creation (good for startup validation)
            # self.test_connection()

        except Exception as e:
            logger.error(f"Failed to initialize the database engine: {e}", exc_info=True)
            raise RuntimeError(f"Database initialization error: {e}") from e

    def get_session(self):
        '''
        Creates and returns a new database session.
        Returns:
            Session: A new SQLAlchemy session object.
        Raises:
            RuntimeError: If session creation fails.
        '''
        logger.info("Creating a new database session...")
        try:
            session = self.Session()
            session.expire_on_commit = False  # often helpful in web apps
            return session
        except SQLAlchemyError as e:
            logger.error(f"Failed to create a database session: {e}", exc_info=True)
            raise RuntimeError(f"Session creation error: {e}") from e
        
    def test_connection(self):
        '''
        Tests the database connection.
        Raises:
            RuntimeError: If the connection test fails.
        '''
        try:
            with self.engine.connect() as conn:
                logger.info("Database connection test successful.")
        except SQLAlchemyError as e:
            logger.error(f"Database connection test failed: {e}", exc_info=True)
            raise RuntimeError(f"Database connection error: {e}") from e

    def create_database_if_not_exists(self):
        '''
        Checks if the database exists and creates it if necessary.
        Returns:
            bool: True if the database was created, False if it already exists.
        Raises:
            RuntimeError: If database existence check or creation fails.
        '''
        from sqlalchemy_utils import database_exists, create_database

        logger.info("Checking if the database exists...")
        try:
            if not database_exists(self.engine.url):
                logger.info(f"Database does not exist. Creating database: {self.engine.url.database}")
                create_database(self.engine.url)
                logger.info("Database created successfully.")
                return True
            else:
                logger.info("Database already exists.")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error during database existence check or creation: {e}", exc_info=True)
            raise RuntimeError(f"Database creation error: {e}") from e

    def tables_exist(self):
        '''
        Checks if any tables exist in the database.
        Returns:
            bool: True if tables exist, False otherwise.
        Raises:
            RuntimeError: If table existence check fails.
        '''
        logger.info("Checking if tables exist in the database...")
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            logger.info(f"Found {len(tables)} tables in database.")
            return len(tables) > 0
        except SQLAlchemyError as e:
            logger.error(f"Error checking table existence: {e}", exc_info=True)
            raise RuntimeError(f"Table existence check error: {e}") from e
# update by zakarya
