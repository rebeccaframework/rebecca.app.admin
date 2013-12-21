from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    relationship,
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
    birthday = Column(Date)
    job_id = Column(Integer, ForeignKey('job.id'))
    job = relationship('Job', backref='persons')

    def __unicode__(self):
        return self.name

    def __html__(self):
        return self.name


class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10))


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(10))


def init(engine):
    DBSession.remove()
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    for i in range(10):
        person = Person(name='person {0:03d}'.format(i))
        DBSession.add(person)
    for i in range(5):
        job = Job(name='job {0:03d}'.format(i))
        DBSession.add(job)
    import transaction
    transaction.commit()
