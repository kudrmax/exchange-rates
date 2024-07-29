import uvicorn
from fastapi import FastAPI

from app.currencies.router import router as currencies_router

app = FastAPI()
app.include_router(currencies_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
