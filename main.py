# main.py
import logging
import time
import threading
from flask import Flask
from API import create_app
import os
from Models.Configuration import Configuration
from Models.DatabaseInitializer import DatabaseInitializer
from Models.Session import DatabaseSession

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    level=logging.INFO,
    format=r'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('application.log', mode='a', encoding='utf-8'),
    ],
)
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel(logging.WARNING)
logger = logging.getLogger('Main')

config = Configuration(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

# Global database session manager
db_session = DatabaseSession(config)

# =========================
# Main Application Entry
# =========================
def main():
    try:
        # =========================
        # Database Initialization
        # =========================
        logger.info("Checking database and tables...")
        if not db_session.create_database_if_not_exists():
            logger.info("Database exists. Checking tables...")
            if not db_session.tables_exist():
                logger.info("Tables missing. Initializing...")
                DatabaseInitializer.initialize_tables(db_session.engine)
                DatabaseInitializer.initialize_records(db_session.get_session())
            else:
                logger.info("All tables already exist.")
                if os.getenv("FORCE_SEED", "false").lower() == "true":
                    logger.info("FORCE_SEED enabled - running seeding despite tables existing")
                    DatabaseInitializer.initialize_records(db_session.get_session())
        else:
            logger.info("Database created successfully. Initializing tables and data...")
            DatabaseInitializer.initialize_tables(db_session.engine)
            DatabaseInitializer.initialize_records(db_session.get_session())

        # =========================
        # Create Flask App
        # =========================
        app = create_app()

        # =========================
        # Start Background Services
        # =========================

        # Flask API Thread
        logger.info('Starting Flask API on http://0.0.0.0:5000')
        flask_thread = threading.Thread(
            target=app.run,
            kwargs={
                'host': '0.0.0.0',
                'port': 6000,
                'debug': True,        # Set to False in production
                'use_reloader': False  # Must be False when running in thread
            },
            name='FlaskAPIThread',
            daemon=True
        )
        flask_thread.start()

        # =========================
        # Keep Main Thread Alive
        # =========================
        logger.info('All services started successfully. Application is running.')
        logger.info('Press Ctrl+C to stop.')

        while True:
                time.sleep(100)

    except Exception as e:
        logger.critical('Fatal error in main application!', exc_info=True)
        raise

# =========================
# Entry Point
# =========================
if __name__ == '__main__':
    main()