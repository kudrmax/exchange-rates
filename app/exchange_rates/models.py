from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Float

from app.database import Base


class MCurrency(Base):
    __tablename__ = 'exchange_rates'

    id = Column(Integer, primary_key=True)
    base_currency_id = Column(ForeignKey('currencies.id'), nullable=False)
    target_currency_id = Column(ForeignKey('currencies.id'), nullable=False)
    rate = Column(Float, nullable=False)
