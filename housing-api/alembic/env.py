import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# On récupère la config Alembic
config = context.config

# Configuration du logging via le fichier .ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import de Base depuis le fichier principal (main.py)
from main import Base
target_metadata = Base.metadata

# 1) Lire la variable d'environnement DATABASE_URL si présente
env_db_url = os.getenv("DATABASE_URL")

if env_db_url:
    # Forcer alembic à utiliser cette URL pour se connecter
    config.set_main_option("sqlalchemy.url", env_db_url)

def run_migrations_offline() -> None:
    """
    Exécuter les migrations en mode 'offline'.
    Dans ce mode, Alembic crée des requêtes SQL
    sans avoir besoin de se connecter réellement.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Exécuter les migrations en mode 'online'.
    On crée un Engine et on associe une connexion
    au contexte de migration.
    """
    # Récupère la section [alembic] de alembic.ini
    # puis crée un engine avec engine_from_config
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # On ouvre la connexion
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Selon le mode (offline/online), on appelle la bonne fonction
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
