from typing import List, Optional

from fastapi import APIRouter

from app.currencies.dao import DAOCurrencies
from app.currencies.schemas import SCurrency, SCurrencyCreate, SCurrencyUpdate
from app.currencies.models import MCurrency

router = APIRouter(
    prefix='/currencies',
    tags=['Валюты']
)


@router.get('/')
async def get_currencies() -> List[SCurrency]:
    return await DAOCurrencies()._get_all()


@router.get('/{id}')
async def get_one_or_none_currencies(id: int) -> Optional[SCurrency]:
    return await DAOCurrencies()._get_one_or_none(id=id)


@router.get('/{code}')
async def get_one_or_none_currencies(code: str) -> Optional[SCurrency]:
    return await DAOCurrencies()._get_one_or_none(code=code)


@router.post('/create')
async def add_currency(currency: SCurrencyCreate) -> None:
    return await DAOCurrencies().create(currency)


@router.put('/update/{id}')
async def update_currency(id: int, currency: SCurrencyUpdate):
    return await DAOCurrencies().update(id, currency)


@router.delete('/delete/{id}')
async def delete_currency(id: int):
    return await DAOCurrencies().delete(id)
