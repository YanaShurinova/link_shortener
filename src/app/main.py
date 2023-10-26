"""Основной модуль."""
from contextlib import asynccontextmanager

import uvicorn
from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from src.app.database import DatabaseConnection
from src.app.repositories.crud import URLRepository
from src.app.schemas import URLSchema

session = DatabaseConnection().get_session()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """lifespan.

    Args:
        app (FastAPI): _description_

    Yields:
        _type_: clien_session
    """
    session_cl = ClientSession()
    yield {'client_session': session_cl}
    await session_cl.close()

app = FastAPI(lifespan=lifespan)


@app.post('/short')
async def short_url(url: URLSchema) -> URLSchema:
    """Хэндлер для запроса сокращения ссылки.

    Args:
        url (URLSchema): исходная ссылка

    Returns:
        URLSchema: новая сокращенная ссылка
    """
    return await URLRepository(session).shorter_url(url)


@app.get('/{url_id}')
async def get_url(url_id: str) -> RedirectResponse:
    """Переадресация.

    Args:
        url_id (str): ключ сокращенной ссылки

    Returns:
        RedirectResponse: переадресация
    """
    long_url = await URLRepository(session).get_url_by_id(url_id)
    return RedirectResponse(long_url)


@app.get('/healthz/ready')
async def ready():
    """Технический обработчик запросов-ready.

    Returns:
        _type_: статус
    """
    session_cl = ClientSession(raise_for_status=True)
    async with session_cl.get('http://localhost:24023/healthz/up') as resp:
        status = resp.status
    if status == HTTP_200_OK:
        if session is not None:
            return HTTP_200_OK
    return HTTP_500_INTERNAL_SERVER_ERROR


@app.get('/healthz/up')
async def up():
    """Технический обработчик запросов-up.

    Returns:
        _type_: статус
    """
    return HTTP_200_OK


if __name__ == 'main':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=24023,
        reload=True,
    )
