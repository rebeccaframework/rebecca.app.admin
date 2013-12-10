from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DummySQLAModel(Base):
    __tablename__ = 'dummy_table'

    id = Column(Integer, primary_key=True)

