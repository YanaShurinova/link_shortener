"""Модуль для обработки запросов."""
from src.app.schemas import URL


async def shorter_url(inp_url: URL) -> str:
    """Метод для сокращения ссылки.

    Args:
        inp_url (URL): исходная ссылка

    Returns:
        str: сокращенная ссылка
    """
    return ' '
