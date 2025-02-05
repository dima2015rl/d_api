from src.auth.models import User
from src.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User
