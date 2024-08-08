from fastapi import HTTPException, status

from app.currencies.router import get_one_or_none_currencies
from app.exchange.schemas import SExchange
from app.exchange_rates.router import get_one_or_none_exchange_rate


class DAOExchange:

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

        # в БД нет ни FT, ни TF, но есть курс F-EUR или EUR-T или T-EUR или EUR-F
        rate_from_eur = None
        pair_from_eur = await get_one_or_none_exchange_rate(code_from + 'EUR', session)
        if pair_from_eur:
            rate_from_eur = pair_from_eur.rate
        else:
            pair_eur_from = await get_one_or_none_exchange_rate('EUR' + code_from, session)
            if pair_eur_from:
                rate_from_eur = 1 / pair_eur_from.rate

        rate_to_eur = None
        pair_to_eur = await get_one_or_none_exchange_rate(code_to + 'EUR', session)
        if pair_to_eur:
            rate_to_eur = pair_to_eur.rate
        else:
            pair_eur_to = await get_one_or_none_exchange_rate('EUR' + code_to, session)
            if pair_eur_to:
                rate_to_eur = 1 / pair_eur_to.rate

        if rate_from_eur and rate_to_eur:
            rate = rate_from_eur / rate_to_eur
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
