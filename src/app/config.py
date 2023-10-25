"""Описание переменных окружения для подключения к БД."""
import os

from dotenv import load_dotenv

load_dotenv()

db_host = os.environ.get('DB_HOST')
db_login = os.environ.get('DB_LOGIN')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')
