from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select

from app.crud import CRUD
from app.currencies.models import MCurrency
from app.currencies.schemas import SCurrency
from app.exchange_rates.models import MExchangeRate
from app.exchange_rates.schemas import SExchangeRatesCreate, SExchangeRates, SExchangeRatesUpdate

import requests

from app.currencies.router import get_one_or_none_currencies, get_all_currencies


class ExchangeRatesDAO(CRUD):
    Model = MExchangeRate

    @classmethod
    async def get_all_with_filter(cls, session, **filter_kwargs):
        query = select(cls.Model).filter_by(**filter_kwargs)
        result = await session.execute(query)
        scalars = result.scalars().all()
        return [await cls._get_pair_schema_by_id(
            obj.base_currency_id,
            obj.target_currency_id,
            session
        ) for obj in scalars]

    @classmethod
    async def get_one_or_none_by_code(cls, session, base_code: str, target_code: str):
        base_currency = await get_one_or_none_currencies(base_code, session)
        target_currency = await get_one_or_none_currencies(target_code, session)
        if not base_currency or not target_currency:
            return None

        query = select(cls.Model).filter_by(base_currency_id=base_currency.id, target_currency_id=target_currency.id)
        result = await session.execute(query)
        scalar = result.scalar()
        if not scalar:
            return None
        return await cls._get_pair_schema_by_id(
            scalar.base_currency_id,
            scalar.target_currency_id,
            session
        )

    @classmethod
    async def get_pair_model_one_or_none_by_code(cls, session, base_currency_code: str, target_currency_code: str):
        base_currency = await get_one_or_none_currencies(base_currency_code, session)
        target_currency = await get_one_or_none_currencies(target_currency_code, session)

        return await cls.get_one_or_none_with_filter(
            session,
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id
        )

    @classmethod
    async def get_pair_model_one_or_none_by_id(cls, session, base_currency_id: int, target_currency_id: int):
        base_currency = await session.get(MCurrency, base_currency_id)
        target_currency = await session.get(MCurrency, target_currency_id)

        return await cls.get_one_or_none_with_filter(
            session,
            base_currency_id=base_currency.id,
            target_currency_id=target_currency.id
        )

    @classmethod
    async def _get_pair_schema_by_code(cls, base_code: str, target_code: str, session) -> Optional[SExchangeRates]:
        pair = await cls.get_pair_model_one_or_none_by_code(session, base_code, target_code)
        if not pair:
            return None
        base_currency = await get_one_or_none_currencies(base_code, session)
        target_currency = await get_one_or_none_currencies(target_code, session)

        return SExchangeRates(
            id=pair.id,
            base_currency=SCurrency(**base_currency.__dict__),
            target_currency=SCurrency(**target_currency.__dict__),
            rate=pair.rate
        )

    @classmethod
    async def _get_pair_schema_by_id(cls, base_code_id: int, target_code_id: int, session) -> Optional[SExchangeRates]:
        pair = await cls.get_pair_model_one_or_none_by_id(session, base_code_id, target_code_id)
        if not pair:
            return None
        base_currency = await session.get(MCurrency, base_code_id)
        target_currency = await session.get(MCurrency, target_code_id)

        return SExchangeRates(
            id=pair.id,
            base_currency=SCurrency(**base_currency.__dict__),
            target_currency=SCurrency(**target_currency.__dict__),
            rate=pair.rate
        )

    @classmethod
    async def update(cls, base_code: str, target_code: str, new_rate: float, session):
        obj = await cls.get_pair_model_one_or_none_by_code(session, base_code, target_code)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'There is no pair with codes {base_code} and {target_code}!'
            )

        obj.rate = new_rate
        await session.commit()
        return await cls._get_pair_schema_by_code(base_code, target_code, session)

    @classmethod
    async def create(cls, new_exchange_rate: SExchangeRatesCreate, session):

        base_currency = await get_one_or_none_currencies(new_exchange_rate.base_currency_code, session)
        target_currency = await get_one_or_none_currencies(new_exchange_rate.target_currency_code, session)

        if not base_currency or not target_currency:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Одна из валют не найдена!')

        if await cls.get_pair_model_one_or_none_by_code(
                session,
                new_exchange_rate.base_currency_code,
                new_exchange_rate.target_currency_code
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

        return await cls._get_pair_schema_by_code(new_exchange_rate.base_currency_code,
                                            new_exchange_rate.target_currency_code,
                                            session)
