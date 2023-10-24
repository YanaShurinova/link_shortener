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
    new_id = ''.join(random.choices(ascii_uppercase + digits + ascii_lowercase, k=10))  # noqa: S311, WPS221, E501
    db_short_url.update({new_id: inp_url})
    new_address = new_address + '/' + new_id  # noqa: WPS336
    return URL(url=new_address)  # noqa: WPS336
