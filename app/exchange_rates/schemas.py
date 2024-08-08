from pydantic import BaseModel
from app.currencies.schemas import SCurrency


class SExchangeRates(BaseModel):
    id: int
    base_currency: SCurrency
    target_currency: SCurrency
    rate: float


class SExchangeRatesCreate(BaseModel):
    base_currency_code: str
    target_currency_code: str
    rate: float


class SExchangeRatesUpdate(BaseModel):
    rate: float
