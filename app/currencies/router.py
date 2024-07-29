from fastapi import APIRouter

from app.currencies.dao import DAOCurrencies

router = APIRouter(
    prefix='/currencies',
    tags=['Валюты']
)


@router.get('/')
async def get_currencies():
    return await DAOCurrencies().get_all()
