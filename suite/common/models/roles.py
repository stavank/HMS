from sqlalchemy import Column, String, BigInteger
from datab import BaseForModels


class Roles (BaseForModels):
    __tablename__ = 'roles'

    name = Column(String)
    id = Column(BigInteger, primary_key=True)
