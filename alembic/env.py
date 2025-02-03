import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debugging: Check if Alembic is loading correctly
print("🔹 Alembic is starting...")

config = context.config

# Debugging: Print Alembic configuration path
if config.config_file_name is not None:
    print(f"🔹 Alembic Config File: {config.config_file_name}")
    fileConfig(config.config_file_name)

# Get database URL from environment OR `alembic.ini`
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🔹 Loaded DATABASE_URL: {DATABASE_URL}")

if not config.get_main_option("sqlalchemy.url") and DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

print(f"🔹 Final sqlalchemy.url in Alembic config: {config.get_main_option('sqlalchemy.url')}")

target_metadata = None  # Modify if using ORM

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    print(f"🔹 Running offline migration with URL: {url}")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    print(f"🔹 Running online migration with URL: {configuration.get('sqlalchemy.url')}")

    connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
