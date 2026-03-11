import logging
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import ArgumentError

# Set up logging
logger = logging.getLogger("Models.Configuration")

class Configuration:
    '''
    A class to manage database configuration.
    Attributes:
        db_config (dict): Dictionary containing database connection details.
    Methods:
        get_database_url(): Generates a database connection URL from the configuration.
    '''
    def __init__(self, user, password, host, port, database):
        '''
        Initializes the Configuration object with database credentials.
        Args:
            user (str): Database username.
            password (str): Database password.
            host (str): Database host (e.g., 'localhost').
            port (str): Database port (e.g., '5432').
            database (str): Database name.
        Raises:
            ValueError: If any required field is missing.
        '''
        logger.info(f"Initializing {self.__class__.__name__}...")
        try:
            if not all([user, password, host, port, database]):
                raise ValueError("All database configuration fields are required.")

            self.db_config = {
                'drivername': 'postgresql',
                'username': user,
                'password': password,
                'host': host,
                'port': port,
                'database': database,
            }
            logger.info("Configuration initialized successfully.")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise

    def get_database_url(self):
        '''
        Generates the database connection URL.
        Returns:
            URL: The SQLAlchemy URL object for the database connection.
        Raises:
            RuntimeError: If the database configuration is invalid.
        '''
        logger.info("Generating database URL...")
        try:
            return URL.create(**self.db_config)
        except ArgumentError as e:
            logger.error(f"Invalid database configuration: {e}")
            raise RuntimeError(f"Invalid database configuration: {e}") from e
