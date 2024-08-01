from typing import List

from sqlalchemy import select, update, delete

from app.currencies.models import MCurrency
from app.database import async_session_maker


class DAOBase:
    model = None
    create_schema = None

    @classmethod
    async def _get_one_or_none(cls, **filter_kwargs) -> model:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_kwargs)
            result = await session.execute(query)
            result = result.scalars().one_or_none()
            return result

    @classmethod
    async def _get_all(cls, **filter_kwargs) -> List[model]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_kwargs)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def _create(cls, new_object):
        # @todo сделать так, чтобы он добавлял сразу много объектов за раз
        async with async_session_maker() as session:
            obj = MCurrency(**new_object.model_dump())
            session.add(obj)
            await session.commit()

    @classmethod
    async def _update(cls, id: int, update_object):
        async with async_session_maker() as session:
            print({**update_object.model_dump()})
            query = update(cls.model).where(cls.model.id == id).values(**update_object.model_dump(exclude_none=True))
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == id)
            await session.execute(query)
            await session.commit()
