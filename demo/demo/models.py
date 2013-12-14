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

    def __unicode__(self):
        return self.name

    def __html__(self):
        return self.name


def init(engine):
    DBSession.remove()
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    for i in range(10):
        person = Person(name='person {0:03d}'.format(i))
        DBSession.add(person)
    import transaction
    transaction.commit()
