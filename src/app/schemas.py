"""Pydantic модели."""
from pydantic import BaseModel


class URL(BaseModel):
    """Модель для ссылки.

    Args:
        BaseModel (_type_): _description_
    """

    url: str
