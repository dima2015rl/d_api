from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends

from src.auth.dependecies import get_current_user
from src.auth.models import User
from src.auth.user_dao import UserDAO
from src.theme.dao.user_incorrect_question_dao import UserIncorrectQuestionDAO
from src.theme.models.user_incorrect_questions import UserIncorrectQuestion
from src.theme.models.user_test_progress import UserTestProgress
from src.theme.question_dao import QuestionDAO
from src.theme.schema import SAnswerBase, SThemeResponse, SQuestionBase, SAnswerCheckRequest, SThemeRequest, \
    SThemeWithQuestions, STestBase, STestCheckRequest
from src.theme.dao.test_dao import TestDAO
from src.theme.dao.theme_dao import ThemeDAO
from src.theme.dao.user_test_progress_dao import UserTestProgressDAO
router = APIRouter(
    prefix="/themes",
    tags=["Работа с темами вопросами и тд тп"]
)


@router.get("",response_model=int, summary="Получить количество тем")
async def get_theme_len():
    return len(await ThemeDAO.find_all())


@router.post("",response_model=SThemeResponse, summary="Получить тему с тестами")
async def get_theme_with_questions(request: SThemeRequest,current_user: User = Depends(get_current_user)):
    theme = await ThemeDAO.get_theme_with_tests(request.theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Тема не найдена")
    if current_user.points<theme.points_to_access:
        return {"message": "У вас недостаточно очков, чтобы отрыть эту тему"}
    return SThemeResponse(
        id=theme.id,
        name=theme.name,
        max_score=theme.max_score,
        tests=[
            STestBase(id=test.id,name=test.name)
            for test in theme.tests  # собираем список всех тестов
        ]
    )


@router.post("/questions/check_answer/", summary="Проверить ответ на вопрос")
async def check_answer(request: SAnswerCheckRequest):
    question = await QuestionDAO.get_question_with_answers(request.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    correct_answer = question.true_answer.answer_id
    if not correct_answer:
        raise HTTPException(status_code=500, detail="У вопроса отсутствует правильный ответ")

    is_correct = correct_answer == request.answer_id
    return {"question_id": request.question_id, "is_correct": is_correct}


@router.post("/questions/check_test/", summary="Проверить тест на правильность")
async def check_answer(request: STestCheckRequest, current_user: User = Depends(get_current_user)):
    # Получаем прогресс пользователя по тесту
    progress = await UserTestProgressDAO.find_one_or_none(user_id=current_user.id, test_id=request.test_id)

    # Если попыток нет и с последней попытки не прошел день
    if progress and progress.attempts_left == 0:
        if progress.last_attempt and datetime.now() - progress.last_attempt < timedelta(minutes=5):
            raise HTTPException(
                status_code=400,
                detail="Попытки закончились. Попробуйте снова через день."
            )
        else:
            # Сбрасываем попытки, если прошел день
            progress.attempts_left = 3

    # Если прогресса нет, создаем новую запись
    if not progress:
        progress = UserTestProgress(
            user_id=current_user.id,
            test_id=request.test_id,
            attempts_left=3
        )
        await UserTestProgressDAO.add(progress)

    # Проверяем ответы на вопросы
    test_result = await TestDAO.test_verification(request.test_id, questions=request.questions)

    if test_result:
        correct_questions = set(test_result["correct_questions"])  # id вопросов, на которые ответили правильно
        wrong_questions = set(test_result["wrong_questions"])  # id вопросов, на которые ответили неправильно

        # 1. Удаляем вопросы, на которые пользователь теперь ответил правильно
        await UserIncorrectQuestionDAO.delete_where(
            user_id=current_user.id,
            question_id=list(correct_questions)  # Удаляем все вопросы, которые теперь правильные
        )

        # 2. Добавляем новые неправильные вопросы, которых нет в базе
        for question_id in wrong_questions:
            if not await UserIncorrectQuestionDAO.find_one_or_none(question_id=question_id, user_id=current_user.id):
                incorrect_question = UserIncorrectQuestion(
                    user_id=current_user.id,
                    question_id=question_id
                )
                await UserIncorrectQuestionDAO.add(incorrect_question)

        # 3. Обновляем лучший результат
        if test_result["correct_points"] >= progress.best_score:
            current_user.points -= progress.best_score
            current_user.balance -= progress.best_score
            progress.best_score = test_result["correct_points"]
            new_points = current_user.points + test_result["correct_points"]
            new_balance = current_user.balance + test_result["correct_points"]
            await UserDAO.update_points_and_balance(current_user.id, new_points, new_balance)

        # 4. Обновляем прогресс
        progress.attempts_left -= 1
        progress.last_attempt = datetime.now()

        # 5. Сохраняем прогресс
        await UserTestProgressDAO.update(
            filter_by={"user_id": current_user.id, "test_id": request.test_id},
            update_data={
                "attempts_left": progress.attempts_left,
                "best_score": progress.best_score,
                "last_attempt": progress.last_attempt
            }
        )

        return test_result



@router.get("/get_test/{test_id}",response_model=SThemeWithQuestions, summary="Получить тест по айди")
async def get_test_by_id(test_id: int, current_user: User = Depends(get_current_user)):
    test = await TestDAO.get_test_with_questions_and_answers(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Тест не найден")
    return SThemeWithQuestions(
        id=test.id,
        name=test.name,
        max_score = test.max_score,
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
