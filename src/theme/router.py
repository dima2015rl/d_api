from fastapi import APIRouter, HTTPException, Depends

from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.theme.theme_progress_dao import ThemeProgressDAO
from src.theme.question_dao import QuestionDAO
from src.theme.schema import SAnswerBase, SThemeResponse, SQuestionBase, SAnswerCheckRequest, SThemeRequest, \
    SThemeWithQuestions
from src.theme.test_dao import TestDAO
from src.theme.theme_dao import ThemeDAO

router = APIRouter(
    prefix="/themes",
    tags=["Работа с темами вопросами и тд тп"]
)


@router.get("", summary="Получить количество тем")
async def get_theme_len():
    return len(await ThemeDAO.find_all())


@router.post("", summary="Получить тему с тестами")
async def get_theme_with_questions(request: SThemeRequest):
    theme = await ThemeDAO.get_theme_with_tests(request.theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    return SThemeResponse(
        id=theme.id,
        name=theme.name,
        tests=[
            {
                "id": test.id,
                "name": test.name

            }
            for test in theme.tests  # собираем список всех тестов
        ]
    )


@router.post("/questions/check_answer/", summary="Проверить ответ на вопрос")
async def check_answer(request: SAnswerCheckRequest):
    question = await QuestionDAO.get_question_with_answers(request.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    correct_answer = question.answers.answer_id
    if not correct_answer:
        raise HTTPException(status_code=500, detail="У вопроса отсутствует правильный ответ")

    is_correct = correct_answer == request.answer_id
    return {"question_id": request.question_id, "is_correct": is_correct}


@router.get("/get_test/{test_id}", summary="Проверить ответ на вопрос")
async def get_test_by_id(test_id: int):
    test = await TestDAO.get_test_with_questions_and_answers(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return SThemeWithQuestions(
        id=test.id,
        name=test.name,
        questions=[
            SQuestionBase(
                id=question.id,
                text=question.text,
                answers=[
                    SAnswerBase(id=answer.id, text=answer.text)
                    for answer in question.shuffled_answers
                ],
            )
            for question in test.shuffled_questions
        ],
    )
