from src.auth.models import User
from src.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def update_points_and_balance(cls, user_id: int, points: int,balance: int):
        await cls.update(
            filter_by={"id": user_id},
            update_data={"points": points, "balance": points}
        )