import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ---- Ajuste de sys.path para achar "src/" quando rodar alembic a partir da raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))           # .../migrations
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---- Carrega o app Flask e o db
from src.main import app, db  # garante que app.config e db.metadata existam

# IMPORTANTE: importe os módulos que **declaram** os models
# (isso registra as tabelas no metadata do SQLAlchemy)
from src.models.user import User
from src.models.franchise import Franchise
from src.models.material import Material
from src.models.difficulty import DifficultyFactor
from src.models.client import Client
from src.models.project import Project, ProjectItem

# Alembic config
config = context.config

# Se tiver alembic.ini com logging, aplica:
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# O metadata que o Alembic deve inspecionar
target_metadata = db.metadata

# Pega a URL do banco direto do Flask (funciona com Postgres e SQLite)
SQLALCHEMY_DATABASE_URI = app.config.get("SQLALCHEMY_DATABASE_URI")
if not SQLALCHEMY_DATABASE_URI:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI não definido no app.config")

def run_migrations_offline() -> None:
    url = SQLALCHEMY_DATABASE_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,          # detecta mudanças de tipo
        compare_server_default=True # detecta defaults
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = SQLALCHEMY_DATABASE_URI

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # para SQLite, o batch mode ajuda em alterações
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=connection.dialect.name == "sqlite",
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()