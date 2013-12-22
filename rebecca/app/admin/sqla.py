import logging
import itertools
import colander as c
from sqlalchemy import types
from sqlalchemy.orm import class_mapper
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import RelationshipProperty
from rebecca.repository.sqla import SQLARepository
from zope.interface import implementer
from .interfaces import (
    IModelAdmin,
    IModelAdminFactory,
    IModelDetail,
)
from .schema import DeferredRelation
from .widget import RelationWidget

logger = logging.getLogger(__name__)


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
        self.sessionmaker = sessionmaker
        # TODO: use inspect primary key
        self.repository = SQLARepository(model,
                                         "id", sessionmaker)

    @property
    def db_session(self):
        return self.sessionmaker

    def items(self):
        return iter(self.repository)

    def __getitem__(self, key):
        logger.debug('traversal {key}'.format(key=key))
        try:
            item = self.repository[key]
            resource = SQLAModelDetail(self, key,
                                       self.model, self.schema,
                                       item, self.db_session)
            logger.debug('{key} {resource}'.format(key=key,
                                                   resource=resource))
            return resource
        except KeyError as e:
            logger.debug('Key Error {e}'.format(e=e))
            raise

    def add(self, values):
        return self.repository.new_item(**values)

    def search_relation(self, relation_name, limit=None, offset=None):
        query = query_relation(self.sessionmaker, self.model, relation_name)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()


@implementer(IModelDetail)
class SQLAModelDetail(object):
    def __init__(self, parent, key, model, schema, item, db_session):
        self.__parent__ = parent
        self.__name__ = self.key = key
        self.model = model
        self.schema = schema
        self.item = item
        self.db_session = db_session

    @property
    def appstruct(self):
        mapper = class_mapper(self.model)
        names = mapper.attrs.keys()
        return {n: getattr(self.item, n) for n in names}


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
    relations = []
    for attr in mapper.attrs:
        if isinstance(attr, RelationshipProperty):
            for local, remote in attr.local_remote_pairs:
                relations.append(local)

    for col in mapper.columns:
        if col.primary_key and col.autoincrement:
            continue

        if col.foreign_keys and col in relations:
            continue

        schema.add(schema_type_mapper(col))

    for attr_name, attr in mapper.attrs.items():
        if isinstance(attr, RelationshipProperty):
            related_to = attr.mapper.class_
            schema.add(c.SchemaNode(DeferredRelation(related_to),
                                    name=attr_name,
                                    widget=RelationWidget(
                                        url='@@search/' + attr_name)))
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
