import uvicorn
from fastapi import FastAPI

from app.currencies.router import router as currencies_router
from app.exchange_rates.router import router as exchange_rates_router
from app.exchange.router import router as exchange_router
from app.parser.router import router as parser_router

app = FastAPI()
app.include_router(currencies_router)
app.include_router(exchange_rates_router)
app.include_router(exchange_router)
app.include_router(parser_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
