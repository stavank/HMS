from sqlalchemy import Column, String, BigInteger
from datab import BaseForModels


class Patients (BaseForModels):
    __tablename__ = 'patients'

    email = Column(String)
    address = Column(String)
    ref_no = Column(String)
    reg_no = Column(String)
    mlc_no = Column(String)
    contact = Column(BigInteger)
    category = Column(String)
    age = Column(String)
    type = Column(String)
    sex = Column(String)
    name = Column(String)
    id = Column(BigInteger, primary_key=True)
