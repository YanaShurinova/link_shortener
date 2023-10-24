"""Модуль для обработки запросов."""
import random
from string import ascii_lowercase, ascii_uppercase, digits

from src.app.database import db_short_url
from src.app.schemas import URL


async def shorter_url(inp_url: URL) -> URL:
    """Метод для сокращения ссылки.

    Args:
        inp_url (URL): исходная ссылка

    Returns:
        URL: сокращенная ссылка
    """
    new_address = 'http://localhost:24023'
    is_validate = await validate_url(inp_url.url)
    if is_validate is None:
        new_id = await create_short_url_id()
        db_short_url.update({new_id: inp_url.url})
        new_address = new_address + '/' + new_id  # noqa: WPS336
    else:
        new_address = new_address + '/' + is_validate  # noqa: WPS336
    return URL(url=new_address)  # noqa: WPS336


async def create_short_url_id() -> str:
    """Метод создания id короткой ссылки.

    Returns:
        str: id короткой ссылки
    """
    flag = True
    while flag:
        new_id = ''.join(random.choices(ascii_uppercase + digits + ascii_lowercase, k=6))  # noqa: S311, WPS221, E501
        if new_id in db_short_url.keys():
            flag = True
        else:
            return new_id


async def validate_url(inp_url: str):
    """Метод валидации исходного url.

    Args:
        inp_url (str): исходный url

    Returns:
        _type_: либо ключ сокращенной ссылки, либо None
    """
    for key, url in list(db_short_url.items()):
        if url == inp_url:
            return key
    return None
