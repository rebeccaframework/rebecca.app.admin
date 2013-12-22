# -*- coding:utf-8 -*-
import colander
from colander.interfaces import Type
import translationstring
from sqlalchemy.orm.exc import (
    MultipleResultsFound,
    NoResultFound,
)


_ = translationstring.TranslationStringFactory('colander')


def DeferredRelation(model):
    def deferred_relation_type(node, kw):
        db_session = kw['db_session']
        return Relation(model, db_session)
    return colander.deferred(deferred_relation_type)


class Relation(Type):
    def __init__(self, model, db_session):
        self.model = model
        self.db_session = db_session

    def query(self):
        return self.db_session.query(self.model)

    def deserialize(self, node, cstruct):
        if cstruct in (colander.null, ''):
            return None

        try:
            return self.query().filter(self.model.id == cstruct).one()
        except NoResultFound:
            raise colander.Invalid(
                node,
                _("${cstruct} is not found from ${model}",
                  mapping={'cstruct': cstruct,
                           'model': self.model.__name__}))
        except MultipleResultsFound:
            raise colander.Invalid(
                node,
                _("${cstruct} is found multiple instance from ${model}",
                  mapping={'cstruct': cstruct,
                           'model': self.model.__name__}))

    def serialize(self, node, appstruct):
        if appstruct == colander.null:
            return colander.null
        if appstruct is None:
            return colander.null
        assert isinstance(appstruct, self.model), appstruct
        return str(appstruct.id)  # TODO: introspection primary key
