import unittest
from testfixtures import compare


class DummyField(object):
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ
        self.called = []

    def renderer(self, *args, **kwargs):
        self.called.append(('renderer', args, kwargs))
        return args, kwargs


class DummyType(object):
    def __init__(self, model):
        self.model = model


class TestRelationWidget(unittest.TestCase):

    def _getTarget(self):
        from ..widget import RelationWidget
        return RelationWidget

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_serialize(self):
        from ..testing import DummySQLAModel
        target = self._makeOne(url='@@search/dummy')
        field = DummyField('dummy', DummyType(DummySQLAModel))
        result = target.serialize(field, "<")

        compare(result,
                (('relation',),
                 {'cstruct': '<',
                  'field': field,
                  'model': 'dummysqlamodel',
                  'url': '@@search/dummy'}))
