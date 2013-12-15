import itertools
import colander as c
from sqlalchemy import types
from sqlalchemy.orm import class_mapper
from sqlalchemy.inspection import inspect
from rebecca.repository.sqla import SQLARepository

from zope.interface import implementer
from .interfaces import IModelAdmin, IModelAdminFactory


@implementer(IModelAdminFactory)
class SQLAModelAdminFactory(object):

    def __init__(self, name, model, sessionmaker, category):
        self.name = name
        self.model = model
        self.schema = create_schema(model)
        self.sessionmaker = sessionmaker
        self.category = category

    def __call__(self, parent):
        admin = SQLAModelAdmin(
            self.name, self.model, self.sessionmaker, self.category)
        admin.__parent__ = parent
        return admin

@implementer(IModelAdmin)
class SQLAModelAdmin(object):

    def __init__(self, name, model, sessionmaker, category):
        self.__name__ = self.name = name
        self.model = model
        self.schema = create_schema(model)
        self.category = category

        # TODO: use inspect primary key
        self.repository = SQLARepository(model,
                                         "id", sessionmaker)

    def items(self):
        return iter(self.repository)

    def __getitem__(self, key):
        return self.repository(key)

    def add(self, values):
        return self.repository.new_item(**values)

    def search_relation(self, relation_name, limit=None, offset=None):
        query = query_relation(self.sessionmaker, self.model, relation_name)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()


class SimpleTypeConvert(object):
    def __init__(self, typ):
        typ = getattr(typ, 'impl', typ)
        self.typ = typ

    def __call__(self, col):
        return c.SchemaNode(self.typ(),
                            name=col.name)


class LengthTypeConvert(object):
    def __init__(self, typ):
        typ = getattr(typ, 'impl', typ)
        self.typ = typ

    def __call__(self, col):
        sqla_type = col.type
        max_len = sqla_type.length
        if max_len:
            validator = c.Length(0, sqla_type.length)
        else:
            validator = None
        return c.SchemaNode(self.typ(),
                            validator=validator,
                            name=col.name)

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

    def __call__(self, col):
        """ convert from sqla type to colander schema type"""
        for col_type, colander_type in default_type_map.items():
            if isinstance(col.type, col_type):
                return colander_type(col)


default_type_mapper = DefaultTypeMapper()


def create_schema(model, schema_type_mapper=default_type_mapper):
    mapper = class_mapper(model)

    schema = c.MappingSchema()

    ## mapper.columnsよりもmapper.attrsのほうが正解か？
    for col in mapper.columns:
        if col.primary_key and col.autoincrement:
            continue

        ## TODO: foreignkey
        # relationship.mapper.class_ プロパティを使う？
        # relationshipの場合は通常のschemaに加えて、検索機能つきのwidgetにする

        schema.add(schema_type_mapper(col))

    return schema


def get_related_model_mapper(model, prop_name):
    mapper = class_mapper(model)
    if not mapper.has_property(prop_name):
        return None
    return mapper.attrs[prop_name].mapper

def query_relation(session, model, prop_name):
    """ search for named relationship property"""

    related_mapper = get_related_model_mapper(model, prop_name)
    if related_mapper is None:
        return
    return session.query(related_mapper.class_)
