"""Интеграционный тест."""
import sys

import pytest
import pytest_asyncio
from aiohttp import ClientSession

from src.app.repositories.crud import URLRepository
from src.app.schemas import URLSchema

sys.path.append('C://Users//Яна//PycharmProjects//shift_course')


@pytest_asyncio.fixture
async def repository(db_session):
    """_summary_.

    Args:
        db_session (_type_): _description_

    Yields:
        _type_: _description_
    """
    yield URLRepository(db_session)


@pytest_asyncio.fixture()
async def create_short_url(repository):
    """_summary_.

    Args:
        repository (_type_): _description_

    Yields:
        _type_: _description_
    """
    url = URLSchema(url='https://learn.microsoft.com/ru-ru/samples/browse/')
    yield await repository.shorter_url(url)


@pytest.mark.asyncio
async def test_main(repository, db_session, create_short_url):
    """_summary_.

    Args:
        repository (_type_): _description_
        db_session (_type_): _description_
        create_short_url (_type_): _description_
    """
    session_cl = ClientSession('http://localhost:24023')
    async with session_cl.get('/healthz/ready') as resp:
        status = resp.status
    assert status == 200
    async with session_cl.get('/healthz/up') as resp:  # noqa: WPS440
        status = resp.status
    assert status == 200
    url_id = await repository.validate_url('https://learn.microsoft.com/ru-ru/samples/browse/')  # noqa: E501
    assert url_id is not None
