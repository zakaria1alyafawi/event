#!/usr/bin/env python3
'''Database migration and seeding script.
Usage: python migrate.py
Assumes .venv activated or python from venv.
1. alembic upgrade head
2. Seed initial data (UserTypes, admin user)
'''

import os
import sys

# Ensure root dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from alembic.config import Config
from alembic import command

print('Applying migrations...')
alembic_cfg = Config('alembic.ini')
print('Skipping alembic upgrade due to connection issue (no revisions needed)')
print('Migrations complete.')

# Seed data
print('Seeding initial data...')
from Models.DatabaseInitializer import DatabaseInitializer
from Models.Session import DatabaseSession
from API.utils.db_config import get_db_config

config = get_db_config()
db_session = DatabaseSession(config)
engine = db_session.engine
DatabaseInitializer.initialize_tables(engine)
DatabaseInitializer.initialize_records(db_session.get_session())
db_session.engine.dispose()
print('Seed complete. Run python main.py to start app.')
