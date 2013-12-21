import unittest
from testfixtures import compare


class DummyField(object):
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ


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
        target = self._makeOne()
        result = target.serialize(DummyField('dummy',
                                             DummyType(DummySQLAModel)),
                                  "<")

        compare(result,
                '<input type="text"'
                ' name="dummy"'
                ' value="&lt;"'
                ' data-model="dummysqlamodel">')
