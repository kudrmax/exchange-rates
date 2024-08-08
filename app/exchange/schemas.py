from pydantic import BaseModel

from app.currencies.schemas import SCurrency


class SExchange(BaseModel):
    base_currency: SCurrency
    target_currency: SCurrency
    rate: float
    amount: float
    converted_amount: float
