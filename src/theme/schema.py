from pydantic import BaseModel
from typing import List


class SThemeRequest(BaseModel):  # для того чтобы получить тему нам нужно только id
    theme_id: int


class SAnswerBase(BaseModel):  # Модель для ответа
    id: int
    text: str


class SQuestionBase(BaseModel):  # Модель для вопроса
    id: int
    text: str
    answers: List[SAnswerBase]


class STestBase(BaseModel):  # Модель для теста
    id: int
    name: str


#
class SAnswerCheckRequest(BaseModel):  # Модель для ответа на вопрос (для проверки правильности ответа)
    question_id: int
    answer_id: int


class SThemeResponse(BaseModel):  # Модель для ответа на запрос темы с тестами
    id: int
    name: str
    tests: List[STestBase]


class SThemeWithQuestions(BaseModel):
    id: int
    name: str
    max_score: int
    questions: List[SThemeRequest]
    questions: List[SQuestionBase]
