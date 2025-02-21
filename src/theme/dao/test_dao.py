import random
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import async_session
from src.dao.base import BaseDAO
from src.theme.models.question import Question
from src.theme.models.question_true_answers import QuestionTrueAnswer
from src.theme.models.test import Test
from src.theme.models.test_questions import TestQuestion
from src.theme.models.wrong_answer import WrongAnswer
from src.theme.schema import SQuestionLightBase


class TestDAO(BaseDAO):
    model = Test

    @classmethod
    async def get_test_with_questions_and_answers(cls, test_id: int) ->Test:
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

    @classmethod
    async def test_verification(cls, test_id: int,questions: List[SQuestionLightBase]):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=test_id).options(selectinload(Test.questions).selectinload(TestQuestion.question)
                                                                    .selectinload(Question.true_answer))
            result = await session.execute(query)
            test = result.scalar_one_or_none()
            if not test:
                raise HTTPException(status_code=404, detail="Тест не найден")
            if test:
                correct_questions = []
                wrong_question_ids = []
                questions_ids = [q.question_id for q in test.questions]
                for q in questions:
                    if q.id not in questions_ids:
                        raise HTTPException(status_code=400, detail=f"Вопрос {q.id} не принадлежит тесту")
                user_answers = {q.id: q.answer.id for q in questions}
                correct_points = 0
                max_points = test.max_score
            for question in (tq.question for tq in test.questions):
                if user_answers.get(question.id) == question.true_answer.answer_id:
                    correct_points += question.points
                    correct_questions.append(question.id)
                else:
                    wrong_question_ids.append(question.id)
            return {"correct_points": correct_points,
                    "max_points": max_points,
                    "test_id": test_id,
                    "percent": int(round((correct_points / max_points) * 100,0)),
                    "wrong_questions": wrong_question_ids,
                    "correct_questions": correct_questions
                    }