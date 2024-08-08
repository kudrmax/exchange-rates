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
                    base_currency = pair.base_currency,
                    target_currency = pair.target_currency,
                    rate = pair.rate,
                    amount = amount,
                    converted_amount = amount * pair.rate
                )

            # в БД нет валютной пары FT, но есть пара TF
        pair = await get_one_or_none_exchange_rate(code_to + code_from, session)
        if pair:
            return

        # в БД нет ни FT, ни TF
        return
