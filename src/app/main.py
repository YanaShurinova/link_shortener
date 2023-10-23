"""Основной модуль."""
from contextlib import asynccontextmanager

import uvicorn
from aiohttp import ClientSession
from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from src.app.crud import shorter_url
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


@app.post('/api/short_url', response_model=URL)
async def short_url(url: URL):
    """Хэндлер для запроса сокращения ссылки.

    Args:
        url (URL): исходная ссылка

    Returns:
        json: новая сокращенная ссылка
    """
    new_url = await shorter_url(url)
    return {
        'url': new_url,
    }


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
