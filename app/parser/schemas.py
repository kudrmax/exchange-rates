from pydantic import BaseModel


class SExchangeRate(BaseModel):
    base_code: str
    base_name: str
    target_code: str  # код валюты (например 'RUB')
    target_name: str  # код валюты (например 'RUB')
    rate: float
