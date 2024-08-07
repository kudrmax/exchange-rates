from typing import List, Optional

from app.database import get_session
from app.exchange_rates.dao import ExchangeRatesDAO

from fastapi import APIRouter, Depends

from app.exchange_rates.schemas import SExchangeRatesCreate

router = APIRouter(
    prefix='/exchange_rates',
    tags=['Курс обмена']
)


@router.get('/')
async def get_all_exchange_rate():
    pass


@router.get('/{base_code}{target_code}')
async def get_exchange_rate(base_code: str, target_code: str):
    pass


@router.post('/')
async def create_exchange_rate(new_exchange_rate: SExchangeRatesCreate, session=Depends(get_session)):
    return await ExchangeRatesDAO.create(new_exchange_rate, session)


@router.patch('/{base_code}{target_code}')
async def update_exchange_rate(base_code: str, target_code: str, update_rate: float):
    pass
