from sqlalchemy import Column, Integer, String

from app.database import Base


class MCurrency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    name = Column(String)
