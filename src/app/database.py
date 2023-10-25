"""Модуль для хранения данных (подключения к БД)."""
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from src.app.config import db_host, db_login, db_name, db_password, db_port

db_short_url = {}

Base: DeclarativeMeta = declarative_base()


class DatabaseConnection:  # noqa: WPS306
    """Класс для подключения к БД."""

    def __init__(self):
        """_summary_."""
        _engine = create_async_engine(  # noqa: WPS122
            url='postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}'.format(
                db_login, db_password, db_host, db_port, db_name,
            ),
        )
        async_session_factory = sessionmaker(
            _engine,  # noqa: WPS121
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self._session_generator = async_scoped_session(
            async_session_factory,
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        """_summary_.

        Returns:
            AsyncSession: _description_
        """
        return self._session_generator()
