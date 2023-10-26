"""Юнит тесты."""
import pytest
import pytest_asyncio

from src.app.repositories.crud import URLRepository
from src.app.schemas import URLSchema


@pytest.mark.asyncio
class TestURLRepository:
    """."""

    @pytest_asyncio.fixture
    async def repository(self, db_session):
        """_summary_.

        Args:
            db_session (_type_): _description_

        Yields:
            _type_: _description_
        """
        yield URLRepository(db_session)

    @pytest.mark.parametrize('url', [
        pytest.param(
            'https://learn.microsoft.com/ru-ru/docs/',
            id='correct example',
        ),
        pytest.param(
            'https://learn.microsoft.com/ru-ru/docs/',
            id='if such erl exists',
        ),
    ])
    async def test_create_url(self, repository, db_session, url):
        """_summary_.

        Args:
            repository (_type_): _description_
            db_session (_type_): _description_
            url (_type_): _description_
        """
        url = URLSchema(url=url)
        record = await repository.shorter_url(url)
        assert isinstance(record.url, str)
