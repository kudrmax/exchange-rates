from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select


class CRUD:
    Model = None

    @classmethod
    async def get_one_or_none_with_filter(cls, session, **filter_kwargs):
        query = select(cls.Model).filter_by(**filter_kwargs)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def get_all_with_filter(cls, session, **filter_kwargs):
        query = select(cls.Model).filter_by(**filter_kwargs)
        result = await session.execute(query)
        return result.scalars().all()

    # @classmethod
    # async def create(cls, session, new_object):
    #     obj = cls.Model(**new_object.model_dump())
    #     session.add(obj)
    #     await session.commit()
    #     await session.refresh(obj)
    #     return obj.__dict__

    # @classmethod
    # async def update(cls, session, code: str, update_object):
    #     obj = await cls.get_one_or_none_with_filter(session, code=code)
    #     if not obj:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #     for key, val in update_object.model_dump(exclude_none=True).items():
    #         setattr(obj, key, val)
    #     await session.commit()
    #     await session.refresh(obj)
    #     return obj.__dict__

    # @classmethod
    # async def delete(cls, session, id: int):
    #     obj = await cls.get_one_or_none_with_filter(session, id=id)
    #     if not obj:
    #         return None
    #     obj_ro_return = obj.__dict__
    #     await session.delete(obj)
    #     await session.commit()
    #     return obj_ro_return
