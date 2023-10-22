"""Основной модуль."""
from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI
from starlette.status import HTTP_200_OK


@asynccontextmanager
async def lifespan(app: FastAPI):
    """lifespan.

    Args:
        app (FastAPI): _description_

    Yields:
        _type_: _description_
    """
    session = ClientSession()
    yield {'client_session': session}
    await session.close()

app = FastAPI(lifespan=lifespan)


@app.get('/healthz/ready')
async def ready():
    """Технический обработчик запросов-ready.

    Returns:
        _type_: статус
    """
    session = ClientSession(raise_for_status=True)
    async with session.get('http://localhost:8000/healthz/up') as resp:
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
