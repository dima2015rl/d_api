from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from database import async_session, Base


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
            if isinstance(data, BaseModel):  # Если данные в формате Pydantic
                data = data.model_dump()
            elif isinstance(data, Base):  # Если данные — объект SQLAlchemy
                session.add(data)
            else:  # Если данные — словарь
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

    @classmethod
    async def delete_where(cls, **filters):
        async with async_session() as session:
            query = delete(cls.model)

            for key, value in filters.items():
                if isinstance(value, list):
                    query = query.where(getattr(cls.model, key).in_(value))
                else:
                    query = query.where(getattr(cls.model, key) == value)

            await session.execute(query)
            await session.commit()

