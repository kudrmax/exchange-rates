from app.dao.base_models import DAOBase
from app.currencies.models import MCurrency


class DAOCurrencies(DAOBase):
    model = MCurrency
