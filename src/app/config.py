"""Описание переменных окружения для подключения к БД."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()
db_host = os.environ.get('DB_HOST')
db_login = os.environ.get('DB_LOGIN')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')


@dataclass
class PostgresConfig:
    """_summary_.

    Returns:
        _type_: _description_
    """

    login: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self):
        """_summary_.

        Returns:
            _type_: _description_
        """
        return '{0}:{1}@{2}:{3}'.format(
            self.login,
            self.password,
            self.host,
            self.port,
        )

    @property
    def uri(self):
        """_summary_.

        Returns:
            _type_: _description_
        """
        return 'postgresql+asyncpg://{0}/{1}'.format(self.url, self.name)


@dataclass
class AppConfig:
    """."""

    postgres: PostgresConfig


app_config = AppConfig(
    postgres=PostgresConfig(  # noqa: S106
        login=db_login,
        password=db_password,
        host=db_host,
        port=db_port,
        name=db_name,
    ),
)
