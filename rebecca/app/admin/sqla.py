import itertools
import colander as c
from sqlalchemy import types
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



default_type_map = {
    types.String: c.String,
    types.Integer: c.Integer,
    types.Unicode: c.String,
    types.Date: c.Date,
    types.DateTime: c.DateTime,
}


class DefaultTypeMapper(object):
    def __init__(self):
        self.mapps = default_type_map

    def __call__(self, typ):
        """ convert from sqla type to colander schema type"""
        for col_type, colander_type in default_type_map.items():
            if isinstance(typ, col_type):
                return colander_type


default_type_mapper = DefaultTypeMapper()


def create_schema(model, schema_type_mapper=default_type_mapper):
    mapper = class_mapper(model)

    schema = c.MappingSchema()
    for col in mapper.columns:
        typ = getattr(col.type, 'impl', col.type)
        schema.add(c.SchemaNode(schema_type_mapper(typ),
                                name=col.name))
    return schema
