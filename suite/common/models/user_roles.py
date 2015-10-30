from sqlalchemy import Column, String, BigInteger
from datab import BaseForModels


class UserRoles (BaseForModels):
    __tablename__ = 'user_roles'

    email = Column(String)
    user_role_id = Column(String)
    id = Column(BigInteger, primary_key=True)
