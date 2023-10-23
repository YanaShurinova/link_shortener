"""Модуль для обработки запросов."""
import random
from string import ascii_lowercase, ascii_uppercase, digits

from src.app.database import db_short_url, db_url
from src.app.schemas import URL


async def shorter_url(inp_url: URL) -> str:
    """Метод для сокращения ссылки.

    Args:
        inp_url (URL): исходная ссылка

    Returns:
        str: сокращенная ссылка
    """
    address = '/'.join(inp_url.url.split('/')[:3])
    long_id = '/'.join(inp_url.url.split('/')[3:])
    db_url.update({long_id: address})
    new_address = 'http://localhost:24023'
    new_id = ''.join(random.choices(ascii_uppercase + digits + ascii_lowercase, k=10))  # noqa: S311, WPS221, E501
    db_short_url.update({long_id: [new_id, new_address]})
    return new_address + '/' + new_id  # noqa: WPS336
