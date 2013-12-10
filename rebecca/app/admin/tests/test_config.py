import unittest
from testfixtures import compare, Comparison as C
from pyramid import testing

class DummySQLAModel(object):
    pass

class Testadd_admin_model(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, *args, **kwargs):
        from ..config import add_admin_model
        return add_admin_model(*args, **kwargs)

    def test_it(self):
        from ..interfaces import IModelAdmin
        from ..sqla import SQLAModelAdmin
        self._callFUT(self.config, DummySQLAModel, name="dummy")
        result = self.config.registry.getUtility(IModelAdmin, name="dummy")



        compare(result, C(SQLAModelAdmin,
                          name='dummy',
                          strict=False,
                          model=DummySQLAModel))
        schema = result.schema
