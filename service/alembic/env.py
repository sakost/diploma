from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine

from alembic import context
from app.models.about_us_models.about_us_model import AboutUsModel
from app.models.announcements_models.announcements_model import AnnouncementsModel
from app.models.base_model import BaseModel
from app.models.coinquotes_models.coinquotes_model import CoinQuoteModel
from app.models.faq_models.faq_item_model import FAQItemModel
from app.models.transparency_models.transparency_model import TransparencyItem
from app.models.whitepaper_models.whitepaper_model import WhitepaperModel
from app.settings import database_settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
target_metadata = [BaseModel.metadata]
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=database_settings.full_url_sync,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(engine: Engine) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    engine = create_engine(database_settings.full_url_sync)
    run_migrations_online(engine)
