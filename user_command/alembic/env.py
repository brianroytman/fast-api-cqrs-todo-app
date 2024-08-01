from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.orm import DeclarativeBase
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
import sys
import os

class Base(DeclarativeBase):
    pass

config = context.config
database_url = os.getenv('DATABASE_URL_WRITE', 'postgresql+asyncpg://postgres:BroytPGDB123!!@write-db:5432/command_db')

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set target_metadata
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
