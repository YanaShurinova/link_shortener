"""Модуль для работы с банковским работником."""
import random
from datetime import datetime, timedelta
from string import ascii_lowercase, ascii_uppercase, digits

from sqlalchemy import insert, select

from src.app.model import URLModel
from src.app.repositories.base import BaseRepository
from src.app.schemas import URLSchema


class URLRepository(BaseRepository):
    """."""

    async def shorter_url(self, inp_url: URLSchema) -> URLSchema:
        """Метод для сокращения ссылки.

        Args:
            inp_url (URLSchema): исходная ссылка

        Returns:
            URLSchema: сокращенная ссылка
        """
        new_address = 'http://localhost:24023'
        is_validate = await self.validate_url(inp_url.url)
        if is_validate is None:
            new_id = await self.create_short_url_id()
            await self._session.execute(
                insert(URLModel).
                values(
                    id=new_id,
                    target_url=inp_url.url,
                    expires=datetime.now() + timedelta(weeks=1),
                ),
            )
            new_address = new_address + '/' + new_id  # noqa: WPS336
        else:
            new_address = new_address + '/' + is_validate  # noqa: WPS336
        return URLSchema(url=new_address)  # noqa: WPS336

    async def create_short_url_id(self) -> str:
        """Метод создания id короткой ссылки.

        Returns:
            str: id короткой ссылки
        """
        flag = True
        while flag:
            new_id = ''.join(random.choices(ascii_uppercase + digits + ascii_lowercase, k=6))  # noqa: S311, WPS221, E501
            url = (await self._session.execute(
                select(URLModel.id).
                select_from(URLModel).
                where(URLModel.id == new_id),
            )).scalar()
            if url is None:
                return new_id

    async def validate_url(self, inp_url: str):
        """Метод валидации исходного url.

        Args:
            inp_url (str): исходный url

        Returns:
            _type_: либо ключ сокращенной ссылки, либо None
        """
        url_id = (await self._session.execute(
            select(URLModel.id).
            select_from(URLModel).
            where(URLModel.target_url == inp_url),
        )).scalar()
        if url_id is not None:
            return url_id
        return None

    async def get_url_by_id(self, inp_id: str) -> str:
        """Метод получения url по id.

        Args:
            inp_id (str): id короткой ссылки

        Returns:
            str: url исходное
        """
        return (await self._session.execute(
            select(URLModel.target_url).
            select_from(URLModel).
            where(URLModel.id == inp_id),
        )).scalar()
