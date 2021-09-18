from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account(Base):
    """The Account class corresponds to the "accounts" database table.
    """
    __tablename__ = 'accounts'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    age = Column(Integer)
    address = Column(String)
    emergency_contact = Column(String)
    allergies = Column(String) # , seperated
    blood_type = Column(String)
    conditions = Column(String) # , seperated
    medications = Column(String) # , seperated
    bmi = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)

    def __getitem__(self, key):
        return str(getattr(self, key))

    def __setitem__(self, key, newValue):
        setattr(self, key, newValue)

    def get_fields(self, fields=None):
        if fields:
            return {a: str(getattr(self, a)) for a in fields}
        else:
            dets = self.__dict__.copy()
            del dets['_sa_instance_state']
            return dets