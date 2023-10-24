"""Интеграционный тест."""
import sys

import pytest
from fastapi.testclient import TestClient

from src.app.main import app

sys.path.append('C://Users//Яна//PycharmProjects//shift_course')

client = TestClient(app)


@pytest.mark.parametrize('url, expected', [
    pytest.param(
        'https://link.springer.com/article/10.1007/s11277-017-5224-x',
        200,
    ),
    pytest.param(
        'https://link.springer.com/article/10.1007/s11277-017-5224-x',
        200,
    ),
])
def test_main(url, expected):
    """Тест основного эндпоинта.

    Args:
        url (_type_): исходный url
        expected (_type_): код ошибки
    """
    response = client.post(
        '/short',
        json={
            'url': url,
        },
    )
    assert response.status_code == expected


@pytest.mark.parametrize('expected', [
    pytest.param(200),
])
def test_ready(expected):
    """Тест технического обработчика.

    Args:
        expected (_type_): код ошибки
    """
    response = client.get(
        '/healthz/ready',
    )
    assert response.status_code == expected


@pytest.mark.parametrize('expected', [
    pytest.param(200),
])
def test_up(expected):
    """Тест технического обработчика.

    Args:
        expected (_type_): код ошибки
    """
    response = client.get(
        '/healthz/up',
    )
    assert response.status_code == expected
