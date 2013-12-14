from sqlalchemy import (
    Column,
    Date,
    Integer,
    Unicode,
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()
DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))


class DummySQLAModel(Base):
    __tablename__ = 'dummy_table'

    id = Column(Integer, primary_key=True)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(10))
    last_name = Column(Unicode(10))
    birthday = Column(Date)
