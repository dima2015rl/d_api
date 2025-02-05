
from sqlalchemy import select

from sqlalchemy.orm import selectinload
from database import async_session
from src.dao.base import BaseDAO

from src.theme.models.theme_progress import ThemeProgress


class ThemeProgressDAO(BaseDAO):
    model = ThemeProgress
