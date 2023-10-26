"""Модуль conftest."""
import asyncio

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.config import app_config
from src.app.database import Base


@pytest.fixture(scope='session')
def event_loop():
    """.

    Yields:
        _type_: _description_
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def config():
    """.

    Yields:
        _type_: _description_
    """
    app_config.postgres.name = '{0}_test'.format(app_config.postgres.name)
    yield app_config


@pytest_asyncio.fixture(scope='session')
async def flush_db(config):  # noqa: WPS217, WPS442
    """_summary_.

    Args:
        config (_type_): _description_

    Yields:
        _type_: _description_
    """
    postgres_table_uri = 'postgresql://{0}/postgres'.format(app_config.postgres.url)  # noqa: E501

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute('DROP DATABASE IF EXISTS {0}_test'.format(app_config.postgres.name))  # noqa: E501
    await connection.execute('CREATE DATABASE {0}_test'.format(app_config.postgres.name))  # noqa: E501
    await connection.close()
    yield
    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute('DROP DATABASE IF EXISTS {0}_test'.format(app_config.postgres.name))  # noqa: E501
    await connection.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine(config):
    """_summary_.

    Args:
        config (_type_): _description_

    Yields:
        _type_: _description_
    """
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='session')
async def new_db_schema(flush_db, db_engine):
    """_summary_.

    Args:
        flush_db (_type_): _description_
        db_engine (_type_): _description_

    Yields:
        _type_: _description_
    """
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_session(new_db_schema, db_engine):
    """_summary_.

    Args:
        new_db_schema (_type_): _description_
        db_engine (_type_): _description_

    Yields:
        _type_: _description_
    """
    pg_session = sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with pg_session() as session, session.begin():  # noqa: WPS316
        yield session
        await session.rollback()
        await session.close()
