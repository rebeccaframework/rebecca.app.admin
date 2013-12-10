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


class SimpleTypeConvert(object):
    def __init__(self, typ):
        self.typ = typ

    def __call__(self, sqla_type):
        return self.typ()


class LengthTypeConvert(object):
    def __init__(self, typ):
        self.typ = typ

    def __call__(self, sqla_type):
        return self.typ()

default_type_map = {
    types.Boolean: SimpleTypeConvert(c.Boolean),
    types.String: LengthTypeConvert(c.String),
    types.Integer: SimpleTypeConvert(c.Integer),
    types.Unicode: LengthTypeConvert(c.String),
    types.Date: SimpleTypeConvert(c.Date),
    types.DateTime: SimpleTypeConvert(c.DateTime),
}


class DefaultTypeMapper(object):
    def __init__(self):
        self.mapps = default_type_map

    def __call__(self, sqla_type):
        """ convert from sqla type to colander schema type"""
        for col_type, colander_type in default_type_map.items():
            if isinstance(sqla_type, col_type):
                return colander_type(sqla_type)


default_type_mapper = DefaultTypeMapper()


def create_schema(model, schema_type_mapper=default_type_mapper):
    mapper = class_mapper(model)

    schema = c.MappingSchema()
    for col in mapper.columns:
        typ = getattr(col.type, 'impl', col.type)
        schema.add(c.SchemaNode(schema_type_mapper(typ),
                                name=col.name))
    return schema
