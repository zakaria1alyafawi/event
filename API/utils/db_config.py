import os
from dotenv import load_dotenv
from Models.Configuration import Configuration

load_dotenv()

def get_db_config():
    """
    Get DB configuration from env vars. Raises ValueError if missing.
    """
    required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    for key in required:
        if not os.getenv(key):
            raise ValueError(f"Missing required env var: {key}")
    
    return Configuration(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )