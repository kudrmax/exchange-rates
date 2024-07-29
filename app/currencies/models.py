from sqlalchemy import Column, Integer

from app.database import Base


class MCurrency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(Integer)
