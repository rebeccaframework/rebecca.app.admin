import unittest
from testfixtures import compare, Comparison as C
from pyramid import testing

class DummySession(object):
    def __cal__(self):
        return

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
        from ..testing import DummySQLAModel
        import colander as c
        self._callFUT(self.config, DummySQLAModel,
                      sessionmaker=DummySession,
                      name="dummy")
        result = self.config.registry.getUtility(IModelAdmin,
                                                 name="dummy")



        compare(result, C(SQLAModelAdmin,
                          name='dummy',
                          strict=False,
                          model=DummySQLAModel))
        schema = result.schema
        id = schema['id']
        compare(id, C(c.SchemaNode,
                      name='id',
                      title='Id',
                      typ=C(c.Integer),
                      children=[],
                      strict=False))

    def test_without_name(self):
        from ..interfaces import IModelAdmin
        from ..sqla import SQLAModelAdmin
        from ..testing import DummySQLAModel
        import colander as c
        self._callFUT(self.config, DummySQLAModel,
                      sessionmaker=DummySession)
        result = self.config.registry.getUtility(IModelAdmin,
                                                 name="dummysqlamodel")



        compare(result, C(SQLAModelAdmin,
                          name='dummysqlamodel',
                          strict=False,
                          model=DummySQLAModel))
        schema = result.schema
        id = schema['id']
        compare(id, C(c.SchemaNode,
                      name='id',
                      title='Id',
                      typ=C(c.Integer),
                      children=[],
                      strict=False))

    def test_by_dotted_name(self):
        from ..interfaces import IModelAdmin
        from ..sqla import SQLAModelAdmin
        import colander as c
        self._callFUT(self.config,
                      sessionmaker=DummySession,
                      model='rebecca.app.admin.testing.DummySQLAModel')
        result = self.config.registry.getUtility(IModelAdmin,
                                                 name="dummysqlamodel")



        compare(result, C(SQLAModelAdmin,
                          name='dummysqlamodel',
                          strict=False))

        schema = result.schema
        id = schema['id']
        compare(id, C(c.SchemaNode,
                      name='id',
                      title='Id',
                      typ=C(c.Integer),
                      children=[],
                      strict=False))
