import unittest
from testfixtures import compare, Comparison as C
from pyramid import testing


class TestAdminSite(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _getTarget(self):
        from ..resources import AdminSite
        return AdminSite

    def _mekOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_iter(self):
        from ..interfaces import IModelAdmin, IAdminSite
        self.config.registry.registerAdapter(DummyModelAdmin(),
                                             [IAdminSite],
                                             IModelAdmin,
                                             name='dummy')
        request = testing.DummyRequest()
        target = self._mekOne(request)

        compare(list(target),
                ['dummy'])

    def test_getitem(self):
        from ..interfaces import IModelAdmin, IAdminSite
        dummy = DummyModelAdmin()
        self.config.registry.registerAdapter(dummy,
                                             [IAdminSite],
                                             IModelAdmin,
                                             name='dummy')
        request = testing.DummyRequest()
        target = self._mekOne(request)

        result = target['dummy']
        compare(result, C(testing.DummyResource))

class DummyModelAdmin(object):
    def __init__(self, name=None, model=None, schema=None, category=None):
        self.name = name
        self.model = model
        self.schema = schema
        self.category = category

    def __call__(self, parent):
        return testing.DummyResource(
            name=self.name,
            model=self.model,
            schema=self.schema,
            category=self.category,
            __parent__=parent)
