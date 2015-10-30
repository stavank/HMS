from sqlalchemy import Column, String, BigInteger, Boolean
from datab import BaseForModels


class Tests (BaseForModels):
    __tablename__ = 'tests'

    available = Column(Boolean)
    price = Column(String)
    category = Column(String)
    code = Column(String)
    type = Column(String)
    description = Column(String)
    name = Column(String)
    id = Column(BigInteger, primary_key=True)
