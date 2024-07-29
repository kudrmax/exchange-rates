from sqlalchemy import select

from app.database import async_session_maker


class DAOBase:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_kwargs)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_all(cls, **filter_kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_kwargs)
            result = await session.execute(query)
            return result.scalars().all()
