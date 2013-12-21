import unittest
from testfixtures import ShouldRaise

class TestRelation(unittest.TestCase):

    def setUp(self):
        from ..testing import _setup
        self.session = _setup()

    def tearDown(self):
        from ..testing import _teardown
        _teardown()

    def _getTarget(self):
        from ..schema import Relation
        return Relation

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_serialize(self):
        from ..testing import DummySQLAModel
        dummy = DummySQLAModel(value=100)
        self.session.add(dummy)
        self.session.flush()
        target = self._makeOne(DummySQLAModel, self.session)
        result = target.serialize(None, dummy)

        self.assertEqual(result, str(dummy.id))

    def test_deserialize(self):
        from ..testing import DummySQLAModel
        dummy = DummySQLAModel(value=100)
        self.session.add(dummy)
        self.session.flush()
        target = self._makeOne(DummySQLAModel, self.session)
        result = target.deserialize(None, str(dummy.id))

        self.assertEqual(result, dummy)

    def test_deserialize_no_instance(self):
        import colander
        from ..testing import DummySQLAModel
        target = self._makeOne(DummySQLAModel, self.session)
        msg = '${cstruct} is not found from ${model}'
        with ShouldRaise(colander.Invalid(None, msg)):
            target.deserialize(None, "a")

    def test_deserialize_empty(self):
        from ..testing import DummySQLAModel
        target = self._makeOne(DummySQLAModel, self.session)
        result = target.deserialize(None, "")

        self.assertIsNone(result)
