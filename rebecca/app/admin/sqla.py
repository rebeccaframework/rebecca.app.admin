import itertools
import colander as c
from sqlalchemy.orm import class_mapper
from sqlalchemy.inspection import inspect
from zope.interface import implementer
from .interfaces import IModelAdmin

@implementer(IModelAdmin)
class SQLAModelAdmin(object):

    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.schema = create_schema(model)


def create_schema(model):
    mapper = class_mapper(model)

    schema = c.MappingSchema()
    for col in mapper.columns:
        schema.add(c.SchemaNode(c.Int,
                                name=col.name))
    return schema
