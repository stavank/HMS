from sqlalchemy import Column, BigInteger
from datab import BaseForModels


class RolesPermissions (BaseForModels):
    __tablename__ = 'roles_permissions'

    permissions_id = Column(BigInteger)
    role_id = Column(BigInteger)
    id = Column(BigInteger, primary_key=True)
