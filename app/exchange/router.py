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
async def foo(code_from: str, code_to: str, amount: float, session=Depends(get_session)):
    """
    {
        "baseCurrency": {
            "id": 0,
            "name": "United States dollar",
            "code": "USD",
            "sign": "$"
        },
        "targetCurrency": {
            "id": 1,
            "name": "Australian dollar",
            "code": "AUD",
            "sign": "A€"
        },
        "rate": 1.45,
        "amount": 10.00,
        "convertedAmount": 14.50
    }

    Получение курса для обмена может пройти по одному из трёх сценариев. Допустим, совершаем перевод из валюты A в валюту B:

    В таблице ExchangeRates существует валютная пара AB - берём её курс
    В таблице ExchangeRates существует валютная пара BA - берем её курс, и считаем обратный, чтобы получить AB
    В таблице ExchangeRates существуют валютные пары USD-A и USD-B - вычисляем из этих курсов курс AB
    """
    return await DAOExchange.exchange(code_from, code_to, amount, session)