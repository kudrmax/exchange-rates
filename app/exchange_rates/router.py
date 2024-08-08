from typing import List, Optional

from app.database import get_session
from app.exchange_rates.dao import ExchangeRatesDAO

from fastapi import APIRouter, Depends

from app.exchange_rates.schemas import SExchangeRatesCreate, SExchangeRatesUpdate

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


@router.patch('/{codes}')
async def update_exchange_rate(codes: str, new_rate: SExchangeRatesUpdate, session=Depends(get_session)):
    base_code = codes[:3]
    target_code = codes[3:6]
    return await ExchangeRatesDAO.update(base_code, target_code, new_rate.rate, session)
