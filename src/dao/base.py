from pydantic import BaseModel
from sqlalchemy import select, insert, update

from database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, data):
        async with async_session() as session:
            if isinstance(data, BaseModel):
                data = data.model_dump()
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, filter_by: dict, update_data: dict):
        async with async_session() as session:
            query = (
                update(cls.model)
                .filter_by(**filter_by)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()

