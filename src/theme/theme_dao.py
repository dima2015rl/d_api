from src.theme.models.answers import Answer
from src.theme.models.question_true_answers import QuestionTrueAnswer

from sqlalchemy import select

from sqlalchemy.orm import selectinload
import random
from database import async_session
from src.dao.base import BaseDAO
from src.theme.models.question import Question
from src.theme.models.test import Test
from src.theme.models.test_questions import TestQuestion
from src.theme.models.theme import Theme


class ThemeDAO(BaseDAO):
    model = Theme

    @classmethod
    async def get_theme_with_tests(cls, theme_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=theme_id).options(
                selectinload(Theme.tests).selectinload(Test.questions).selectinload(TestQuestion.question)
            )
            result = await session.execute(query)
            theme = result.scalar_one_or_none()
            return theme
