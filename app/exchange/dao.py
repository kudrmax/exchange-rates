from fastapi import HTTPException, status

from app.currencies.router import get_one_or_none_currencies
from app.exchange.schemas import SExchange
from app.exchange_rates.router import get_one_or_none_exchange_rate


class DAOExchange:

    @classmethod
    # async def get_pair_schema(cls, base_code, target_code, session):
    #     base_currency, target_currency = get_one_or_none_exchange_rate(base_code, target_code)
    #     return SExchange(
    #         base_currency = SCurrency(**base_currency.__dict__),
    #         target_currency = SCurrency(**target_currency.__dict__),
    #         rate = None,
    #         amount = None,
    #         converted_amount = None
    #     )

    @classmethod
    async def exchange(cls, code_from: str, code_to: str, amount: float, session):
        pair = await get_one_or_none_exchange_rate(code_from + code_to, session)

        # в БД есть валютная пара FT
        if pair:
            return SExchange(
                base_currency=pair.base_currency,
                target_currency=pair.target_currency,
                rate=pair.rate,
                amount=amount,
                converted_amount=amount * pair.rate
            )

        # в БД нет валютной пары FT, но есть пара TF
        pair = await get_one_or_none_exchange_rate(code_to + code_from, session)
        if pair:
            return SExchange(
                base_currency=pair.target_currency,
                target_currency=pair.base_currency,
                rate=pair.rate,
                amount=amount,
                converted_amount=amount / pair.rate
            )

        # есть курс А-USD или USD-A
        rate_from_usd = None
        pair_from_usd = await get_one_or_none_exchange_rate(code_from + 'USD', session)
        if pair_from_usd:
            rate_from_usd = pair_from_usd.rate
        else:
            pair_usd_from = await get_one_or_none_exchange_rate('USD' + code_from, session)
            if pair_usd_from:
                rate_from_usd = 1 / pair_usd_from.rate

        rate_to_usd = None
        pair_to_usd = await get_one_or_none_exchange_rate(code_to + 'USD', session)
        if pair_to_usd:
            rate_to_usd = pair_to_usd.rate
        else:
            pair_usd_to = await get_one_or_none_exchange_rate('USD' + code_to, session)
            if pair_usd_to:
                rate_to_usd = 1 / pair_usd_to.rate

        if rate_from_usd and rate_to_usd:
            rate = rate_from_usd / rate_to_usd
            base_currency = (await get_one_or_none_currencies(code_from, session)).__dict__
            target_currency = (await get_one_or_none_currencies(code_to, session)).__dict__
            return SExchange(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate,
                amount=amount,
                converted_amount=amount * rate
            )

        # в БД нет ни FT, ни TF
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no exchange rate for {code_from} and {code_to}!"
        )
