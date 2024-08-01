from pydantic import BaseModel


class SCurrency(BaseModel):
    id: int
    code: str
    name: str | None = None


class SCurrencyCreate(BaseModel):
    code: str
    name: str | None = None


class SCurrencyUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
