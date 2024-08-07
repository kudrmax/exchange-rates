from fastapi import HTTPException, status
from sqlalchemy import select

from app.crud import CRUD
from app.currencies.models import MCurrency
from app.currencies.schemas import SCurrencyCreate, SCurrencyUpdate


class DAOCurrencies(CRUD):
    Model = MCurrency

    @staticmethod
    def _is_code_correct(code: str) -> bool:
        return not (len(code) != 3 or not code.isalpha())

    @classmethod
    async def get_one_or_none_by_code(cls, session, code: str):
        if not cls._is_code_correct(code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Code must be exectly 3 letter.')
        query = select(cls.Model).filter_by(code=code.upper())
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def create(cls, session, new_object: SCurrencyCreate):
        code = new_object.code
        if not cls._is_code_correct(code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Code must be exectly 3 letter.')
        if await cls.get_one_or_none_with_filter(session, code=code.upper()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Object with {code=} already exists.')
        obj = cls.Model(**new_object.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj.__dict__

    @classmethod
    async def update(cls, session, code: str, update_object: SCurrencyUpdate):
        obj = await cls.get_one_or_none_with_filter(session, code=code)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if not cls._is_code_correct(update_object.code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Code must be exectly 3 letter.')
        if update_object.code:
            second_obj = await cls.get_one_or_none_with_filter(session, code=update_object.code)
            if second_obj:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'Object with code={update_object.code} already exists.')
        for key, val in update_object.model_dump(exclude_none=True).items():
            setattr(obj, key, val)
        await session.commit()
        await session.refresh(obj)
        return obj.__dict__

    @classmethod
    async def delete(cls, session, code: str):
        if not cls._is_code_correct(code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Code must be exectly 3 letter.')
        obj = await cls.get_one_or_none_with_filter(session, code=code)
        if not obj:
            return None
        obj_ro_return = obj.__dict__
        await session.delete(obj)
        await session.commit()
        return obj_ro_return
