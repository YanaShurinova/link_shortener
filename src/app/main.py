"""Основной модуль."""
from contextlib import asynccontextmanager

import uvicorn
from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_200_OK

from src.app.crud import shorter_url
from src.app.database import db_short_url
from src.app.schemas import URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    """lifespan.

    Args:
        app (FastAPI): _description_

    Yields:
        _type_: clien_session
    """
    session = ClientSession()
    yield {'client_session': session}
    await session.close()

app = FastAPI(lifespan=lifespan)


@app.post('/short')
async def short_url(url: URL) -> URL:
    """Хэндлер для запроса сокращения ссылки.

    Args:
        url (URL): исходная ссылка

    Returns:
        URL: новая сокращенная ссылка
    """
    return await shorter_url(url)


@app.get('/{url_id}')
async def get_url(url_id: str) -> RedirectResponse:
    """Переадресация.

    Args:
        url_id (str): ключ сокращенной ссылки

    Returns:
        RedirectResponse: переадресация
    """
    long_url = db_short_url.get(url_id)
    return RedirectResponse(long_url.url)


@app.get('/healthz/ready')
async def ready():
    """Технический обработчик запросов-ready.

    Returns:
        _type_: статус
    """
    session = ClientSession(raise_for_status=True)
    async with session.get('http://localhost:24023/healthz/up') as resp:
        status = resp.status
    if status == HTTP_200_OK:
        return HTTP_200_OK


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
