from typing import List
from datetime import date, datetime
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from app.currencies.schemas import SCurrencyCreate
from app.exchange_rates.schemas import SExchangeRatesCreate
from app.parser.schemas import SExchangeRate
from app.currencies.router import get_one_or_none_currencies, add_currency
from app.exchange_rates.router import get_one_or_none_exchange_rate, create_exchange_rate


class CurrencyParserBase(ABC):
    """
    Абсрактный класс для парсинга, который обязывает наследников реализовывать метод parse.
    """

    @staticmethod
    def _get_soup(url: str, encoding: str | None = None) -> BeautifulSoup:
        """
        Парсит HTML-код страницы по указанному URL.

        Parameters
        ----------
        url : str
            URL страницы, которую нужно парсить.
        encoding : str, optional
            Кодировка страницы, если она отличается от стандартной.

        Returns
        -------
        BeautifulSoup
            Объект BeautifulSoup для дальнейшего работы со страницей
        """
        response = requests.get(url)
        if encoding is not None:
            response.encoding = encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


class RateParser(CurrencyParserBase):
    url = "https://www.iban.com/exchange-rates"

    @classmethod
    def get_rates_to_eur(cls) -> List[SExchangeRate]:
        rates = []
        soup = cls._get_soup(url=cls.url, encoding='cp1251')
        table = soup.find('table', {'class': 'table table-bordered table-hover downloads'})
        if table:
            for row in table.find('tbody').find_all('tr'):
                columns = row.find_all('td')
                if len(columns) >= 3:
                    currency_code = columns[0].text.strip()[-3:]
                    currency_name = columns[1].text.strip()
                    rate_ro_eur = columns[2].text.strip()
                    try:
                        rate = SExchangeRate(
                            base_code=currency_code,
                            base_name=currency_name,
                            target_code='EUR',
                            target_name='Euro',
                            rate=rate_ro_eur)
                        rates.append(rate)
                    except ValueError as ex:
                        print(f"Error parsing row {row}: {ex}")
        return rates


class DAOFillDatabase:

    @classmethod
    async def load_to_database(self, session):
        rates = RateParser.get_rates_to_eur()

        if not await get_one_or_none_currencies('EUR', session):
            await add_currency(SCurrencyCreate(
                code='EUR',
                name='Euro'
            ), session)

        for rate in rates:

            # если валюты нет в БД валют, то загрузить
            if not await get_one_or_none_currencies(rate.base_code, session):
                await add_currency(SCurrencyCreate(
                    code=rate.base_code,
                    name=rate.base_name
                ), session)
                print(f'Currency {rate.base_code} added to database')

            # если обменного курса нет в БД валют, то загрузить
            pair = await get_one_or_none_exchange_rate(rate.base_code + rate.target_code, session)
            if not pair:
                await create_exchange_rate(SExchangeRatesCreate(
                    base_currency_code=rate.base_code,
                    target_currency_code=rate.target_code,
                    rate=rate.rate
                ), session)
                print(f'Exchange rate between {rate.base_code} and {rate.target_code} added to database')


if __name__ == '__main__':  # для отдельного теста парсинга
    pass
