from sqlalchemy import (
    Column,
    Date,
    Integer,
    Unicode,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DummySQLAModel(Base):
    __tablename__ = 'dummy_table'

    id = Column(Integer, primary_key=True)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(10))
    last_name = Column(Unicode(10))
    birthday = Column(Date)
