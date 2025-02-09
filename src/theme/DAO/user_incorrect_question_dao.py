from src.dao.base import BaseDAO
from src.theme.models.user_incorrect_questions import UserIncorrectQuestion


class UserIncorrectQuestionDAO(BaseDAO):
    model = UserIncorrectQuestion
