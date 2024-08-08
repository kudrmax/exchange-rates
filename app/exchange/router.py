from typing import List, Optional

from app.database import get_session
from app.exchange.dao import DAOExchange
from app.exchange_rates.dao import ExchangeRatesDAO

from fastapi import APIRouter, Depends

from app.exchange_rates.schemas import SExchangeRatesCreate, SExchangeRatesUpdate

router = APIRouter(
    prefix='/exchange',
    tags=['Обмен валют']
)


@router.get('/')
async def get_exchange(code_from: str, code_to: str, amount: float, session=Depends(get_session)):
    """
    В таблице ExchangeRates существуют валютные пары USD-A и USD-B - вычисляем из этих курсов курс AB
    """
    return await DAOExchange.exchange(code_from, code_to, amount, session)