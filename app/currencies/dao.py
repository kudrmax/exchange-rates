from http import HTTPStatus

from fastapi import HTTPException, status
from sqlalchemy import select, update

from app.dao.base_models import DAOBase
from app.currencies.models import MCurrency
from app.currencies.schemas import SCurrencyCreate, SCurrencyUpdate
from app.database import async_session_maker


class DAOCurrencies(DAOBase):
    model = MCurrency
    create_schema = SCurrencyCreate

    @classmethod
    async def create(cls, new_object: SCurrencyCreate):
        return cls._create(new_object)

    @classmethod
    async def update(cls, id: int, new_object: SCurrencyUpdate):
        return cls._update(id, new_object)
