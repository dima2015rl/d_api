from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session

from src.dao.base import BaseDAO
from src.theme.models.question import Question


class QuestionDAO(BaseDAO):
    model = Question

    @classmethod
    async def get_question_with_answers(cls, question_id: int):
        async with async_session() as session:
            query = (
                select(cls.model)
                .filter_by(id=question_id).options(selectinload(Question.true_answer))
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
