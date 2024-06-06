import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import database_settings


APP_NAME = "bureau_1440_test_task"


def make_async_engine(
    database_url: str | URL = database_settings.full_url_async,
) -> AsyncEngine:
    return create_async_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=0,
        connect_args={
            "timeout": database_settings.timeout,
            "server_settings": {
                "statement_timeout": str(database_settings.statement_timeout),
                "application_name": APP_NAME,
            },
        },
    )


def make_async_session_factory(
    database_url: str = database_settings.full_url_async,
    engine: AsyncEngine | None = None,
) -> async_sessionmaker[AsyncSession]:
    engine = engine or make_async_engine(database_url)

    return async_sessionmaker(
        engine,
        autoflush=False,
        autocommit=False,
    )


def make_async_scoped_session_factory(
    database_url: str = database_settings.full_url_async,
) -> async_scoped_session[AsyncSession]:
    session_factory = make_async_session_factory(database_url)
    return async_scoped_session(session_factory, scopefunc=asyncio.current_task)


def make_async_scoped_session(
    database_url: str = database_settings.full_url_async,
) -> AsyncSession:
    # noinspection PyShadowingNames
    AsyncSession = make_async_scoped_session_factory(  # pylint: disable=W0621,C0103,
        database_url
    )
    return AsyncSession()


async_scoped_session_factory = make_async_scoped_session_factory()
async_session_factory = make_async_session_factory()


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_scoped_session_factory() as session:
        yield session
