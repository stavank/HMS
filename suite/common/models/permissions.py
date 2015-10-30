from sqlalchemy import Column, String, BigInteger
from datab import BaseForModels


class Permissions (BaseForModels):
    __tablename__ = 'permissions'

    name = Column(String)
    id = Column(BigInteger, primary_key=True)
