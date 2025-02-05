from sqlalchemy import select

from database import async_session
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

    @classmethod
    async def getliders(cls):
        async with async_session() as session:
            query = select(User).order_by(User.points.desc()).limit(10)
            result = await session.execute(query)
            return result.scalars().all()


