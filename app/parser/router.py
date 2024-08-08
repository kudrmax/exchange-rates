from typing import List, Optional

from app.database import get_session
from app.exchange_rates.dao import ExchangeRatesDAO

from fastapi import APIRouter, Depends

from app.exchange_rates.schemas import SExchangeRatesCreate, SExchangeRatesUpdate
from app.parser.dao import DAOFillDatabase

router = APIRouter(
    prefix='/parse',
    tags=['Парсер валют и обменного курса']
)


@router.get('/')
async def fill_database(session=Depends(get_session)):
    return await DAOFillDatabase.load_to_database(session)