from fastapi import HTTPException, status
from sqlalchemy import select

from app.crud import CRUD
from app.currencies.schemas import SCurrency
from app.exchange_rates.models import MExchangeRate
from app.exchange_rates.schemas import SExchangeRatesCreate, SExchangeRates

import requests

from app.currencies.router import get_one_or_none_currencies, get_currencies


class ExchangeRatesDAO(CRUD):
    Model = MExchangeRate

    @classmethod
    async def get_all(cls):
        return None

    @classmethod
    async def create(cls, new_exchange_rate: SExchangeRatesCreate, session):

        # base_currency = requests.get(f'http://0.0.0.0:8000/currencies/{new_exchange_rate.base_currency_code}')
        # target_currency = requests.get(f'http://0.0.0.0:8000/currencies/{new_exchange_rate.target_currency_code}')

        base_currency = await get_one_or_none_currencies(new_exchange_rate.base_currency_code, session)
        target_currency = await get_one_or_none_currencies(new_exchange_rate.target_currency_code, session)

        if not base_currency or not target_currency:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Одна из валют не найдена!')

        if await cls.get_one_or_none_with_filter(
                session,
                base_currency_id=base_currency.id,
                target_currency_id=target_currency.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'Pair with codes {new_exchange_rate.base_currency_code} and {new_exchange_rate.target_currency_code} already exists.'
            )

        obj = cls.Model(
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id,
            rate=new_exchange_rate.rate
        )
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

        return_obj = SExchangeRates(
            id=obj.id,
            base_currency=SCurrency(**base_currency.__dict__),
            target_currency=SCurrency(**target_currency.__dict__),
            rate=new_exchange_rate.rate
        )

        return return_obj
