from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

async_session_maker = sessionmaker(class_=AsyncSession, expire_on_commit=False)

DB_NAME = 'postgres'
DB_HOST = '0.0.0.0'
DB_PORT = 8000
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_session_maker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Пустая модель SQLAlchemy от которой мы будем наследоваться и использовать ее в Alembic"""
    pass
