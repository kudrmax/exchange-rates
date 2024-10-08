from typing import List, Optional

from fastapi import APIRouter, Depends

from app.currencies.dao import DAOCurrencies
from app.currencies.schemas import SCurrency, SCurrencyCreate, SCurrencyUpdate
from app.database import get_session

router = APIRouter(
    prefix='/currencies',
    tags=['Валюты']
)


@router.get('/')
async def get_all_currencies(session=Depends(get_session)) -> List[SCurrency]:
    return await DAOCurrencies().get_all_with_filter(session)

@router.get('/{code}')
async def get_one_or_none_currencies(code: str, session=Depends(get_session)) -> Optional[SCurrency]:
    return await DAOCurrencies().get_one_or_none_by_code(session, code=code)


@router.post('/')
async def add_currency(currency: SCurrencyCreate, session=Depends(get_session)) -> Optional[SCurrency]:
    return await DAOCurrencies().create(session, currency)


@router.patch('/{code}')
async def update_currency(code: str, currency: SCurrencyUpdate, session=Depends(get_session)) -> Optional[SCurrency]:
    return await DAOCurrencies().update(session, code, currency)


@router.delete('/{code}')
async def delete_currency(code: str, session=Depends(get_session)) -> Optional[SCurrency]:
    return await DAOCurrencies().delete(session, code)
