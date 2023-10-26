"""Модель для бд."""
from sqlalchemy import Column, DateTime, String

from src.app.database import Base


class URLModel(Base):
    """Таблица для бд.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'urls'

    id = Column(String, primary_key=True)
    target_url = Column(String, nullable=False)
    expires = Column(DateTime, nullable=False)
