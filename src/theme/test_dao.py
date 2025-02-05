import random

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session
from src.dao.base import BaseDAO
from src.theme.models.test import Test


class TestDAO(BaseDAO):
    model = Test

    @classmethod
    async def get_test_with_questions_and_answers(cls, test_id: int):
       '''' async with async_session() as session:
            query = select(cls.model).filter_by(id=test_id).options(
                selectinload(Test.questions).
                selectinload(TestQuestion.question).
                selectinload(Question.answers).
                selectinload(QuestionAnswer.answer)
            )
        result = await session.execute(query)
        test = result.scalar_one_or_none()
        if test:
            questions = [tq.question for tq in test.questions]
            random.shuffle(questions)
            test.shuffled_questions = questions
            for question in questions:
                # Берем правильный ответ из связи QuestionAnswer
                correct_answer = question.answers.answer  # Здесь `answers` — это объект QuestionAnswer

                # Получаем остальные ответы, исключая правильный
                other_answers_query = select(Answer).filter(Answer.id != correct_answer.id)
                other_answers_result = await session.execute(other_answers_query)
                other_answers = other_answers_result.scalars().all()
                random.shuffle(other_answers)
                # Формируем список из неправильных ответов + правильного
                selected_answers = other_answers[:3] + [correct_answer]
                random.shuffle(selected_answers)

                # Присваиваем выбранные ответы вопросу
                question.shuffled_answers = selected_answers
        return test'''
       return 2
