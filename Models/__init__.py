import logging
from logging.handlers import RotatingFileHandler

# Set up logging for the Models package (console and file with rotation)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        RotatingFileHandler("application.log", maxBytes=5 * 1024 * 1024, backupCount=3),  # Log to file
    ],
)
logger = logging.getLogger("Models")

logger.info("Models package initialized.")

from .Configuration import Configuration
from .Session import DatabaseSession

__all__ = ["Configuration", "DatabaseSession"]
