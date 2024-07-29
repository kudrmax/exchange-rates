from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_NAME = 'postgres'
DB_HOST = '0.0.0.0'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Пустая модель SQLAlchemy от которой мы будем наследоваться и использовать ее в Alembic"""
    pass
