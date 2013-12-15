from sqlalchemy import (
    Column,
    Date,
    Integer,
    Unicode,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    relationship,
)
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()
DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))

def _setup():
    engine = create_engine('sqlite:///')
    DBSession.remove()
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def _teardown():
    import transaction
    transaction.abort()
    DBSession.remove()
    Base.metadata.drop_all(bind=DBSession.bind)

class DummySQLAModel(Base):
    __tablename__ = 'dummy_table'

    id = Column(Integer, primary_key=True)
    value = Column(Integer)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(10))
    last_name = Column(Unicode(10))
    birthday = Column(Date)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id'))
    job = relationship('Job')

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50))

    def __str__(self):
        return "Job id={self.id} name={self.name}".format(self=self)
