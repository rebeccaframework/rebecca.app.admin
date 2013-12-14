from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10))


def init(engine):
    DBSession.remove()
    DBSession.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
