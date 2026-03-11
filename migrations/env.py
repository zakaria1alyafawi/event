from logging.config import fileConfig
import os
import sys

from sqlalchemy import engine_from_config, pool, create_engine

from alembic import context

# Ensure root dir in path
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.Base import Base
from API.utils.db_config import get_db_config

# Alembic Config
config = context.config

# Logging - COMMENTED
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata

def get_engine_url():
    print("CWD:", os.getcwd())
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    cfg = get_db_config()
    url = str(cfg.get_database_url())
    print("URL:", url)
    return url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_engine_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = get_engine_url()
    connectable = create_engine(
        url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
    )
    print("Engine created")

    with connectable.connect() as connection:
        print("Connected success")
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
