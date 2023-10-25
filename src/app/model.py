"""Модель для бд."""
from sqlalchemy import Column, Integer, String

from src.app.database import Base


class URL(Base):
    """Таблица для бд.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    target_url = Column(String, nullable=False)
