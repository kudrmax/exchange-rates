from contextlib import contextmanager
from typing import AsyncIterator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_NAME = 'postgres'
DB_HOST = '0.0.0.0'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
# Base.metadata.create_all(bind=engine)

# SessionLocal = sessionmaker(
#     engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
# )
# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()


class Base(DeclarativeBase):
    """Пустая модель SQLAlchemy от которой мы будем наследоваться и использовать ее в Alembic"""
    pass
