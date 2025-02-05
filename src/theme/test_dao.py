import random
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.testing.plugin.plugin_base import options

from database import async_session
from src.dao.base import BaseDAO
from src.theme.models.question import Question
from src.theme.models.question_true_answers import QuestionTrueAnswer
from src.theme.models.test import Test
from src.theme.models.test_questions import TestQuestion
from src.theme.models.wrong_answer import WrongAnswer


class TestDAO(BaseDAO):
    model = Test

    @classmethod
    async def get_test_with_questions_and_answers(cls, test_id: int):
        async with (async_session() as session):
            # Формируем запрос для получения теста с вопросами
            query = select(cls.model).filter_by(id=test_id).options(
                selectinload(Test.questions).selectinload(TestQuestion.question)# Загружаем вопросы
            )
            result = await session.execute(query)
            test = result.scalar_one_or_none()

            if test:
                # Перемешиваем вопросы
                questions = [tq.question for tq in test.questions]
                random.shuffle(questions)
                test.shuffled_questions = questions
                for question in questions:
                    correct_answer_query = select(QuestionTrueAnswer).filter_by(question_id=question.id).options(selectinload(QuestionTrueAnswer.answer))
                    correct_answer_result = await session.execute(correct_answer_query)
                    correct_answer = correct_answer_result.scalar_one_or_none().answer

                    #подружаем неправильные ответы
                    wrong_answers_query = select(WrongAnswer).filter_by(question_id=question.id).options(selectinload(WrongAnswer.answer))
                    wrong_answers_result = await session.execute(wrong_answers_query)
                    wrong_answers = [wa.answer for wa in wrong_answers_result.scalars().all()]
                    # Перемешиваем правильный ответ с неправильными
                    selected_answers = wrong_answers + [correct_answer]
                    random.shuffle(selected_answers)

                    # Присваиваем перемешанные ответы вопросу
                    question.shuffled_answers = selected_answers



        return test
