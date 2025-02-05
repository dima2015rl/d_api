from src.theme.models.answers import Answer
from src.theme.models.question_answers import QuestionAnswer

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
                selectinload(Theme.tests)
            )
            # Выполняем запрос асинхронно  '''.selectinload(Test.questions)
            #                 .selectinload(TestQuestion.question)
            #                 .selectinload(Question.answers)
            #                 .selectinload(QuestionAnswer.answer)  # Подгружаем объект ответа'''
            result = await session.execute(query)
            theme = result.scalar_one_or_none()
            '''
            if theme:
             
                for test in theme.tests:
                    questions = [tq.question for tq in test.questions]
                    random.shuffle(questions)
                    test.shuffled_questions = questions
                    for question in questions:
                        # Берем правильный ответ из связи QuestionAnswer
                        correct_answer = question.answers.answer  # Здесь `answers` — это объект QuestionAnswer

                        # Получаем остальные ответы, исключая правильный
                        other_answers_query = select(Answer).filter(Answer.id != correct_answer.id).limit(3)
                        other_answers_result = await session.execute(other_answers_query)
                        other_answers = other_answers_result.scalars().all()

                        # Формируем список из неправильных ответов + правильного
                        selected_answers = other_answers + [correct_answer]
                        random.shuffle(selected_answers)

                        # Присваиваем выбранные ответы вопросу
                        question.shuffled_answers = selected_answers
                        '''
            return theme
