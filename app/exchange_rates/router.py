from typing import List, Optional

SCreateExchangeRate = None

from fastapi import APIRouter

router = APIRouter(
    prefix='/exchange_rates',
    tags=['Курс обмена']
)


@router.get('/')
async def get_all_exchange_rate():
    pass


@router.get('/{base_code}{target_code}')
async def get_exchange_rate(base_code: str, target_code: str):
    pass


@router.post('/')
async def create_exchange_rate(new_exchange_rate: SCreateExchangeRate):
    pass


@router.patch('/{base_code}{target_code}')
async def update_exchange_rate(base_code: str, target_code: str, update_rate: float):
    pass
