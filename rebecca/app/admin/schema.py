# -*- coding:utf-8 -*-
import colander
from colander.interfaces import Type
import translationstring
from sqlalchemy.orm.exc import (
    MultipleResultsFound,
    NoResultFound,
)


_ = translationstring.TranslationStringFactory('colander')


class Relation(Type):
    def __init__(self, model, db_session):
        self.model = model
        self.db_session = db_session

    def query(self):
        return self.db_session.query(self.model)

    def deserialize(self, node, cstruct):
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
        assert isinstance(appstruct, self.model)
        return str(appstruct.id)  # TODO: introspection primary key
