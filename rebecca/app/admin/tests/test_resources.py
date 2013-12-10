import unittest
from testfixtures import compare
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
        from ..interfaces import IModelAdmin
        self.config.registry.registerUtility(DummyModelAdmin(),
                                             IModelAdmin,
                                             name='dummy')
        request = testing.DummyRequest()
        target = self._mekOne(request)

        compare(list(target),
                ['dummy'])

    def test_getitem(self):
        from ..interfaces import IModelAdmin
        dummy = DummyModelAdmin()
        self.config.registry.registerUtility(dummy,
                                             IModelAdmin,
                                             name='dummy')
        request = testing.DummyRequest()
        target = self._mekOne(request)

        result = target['dummy']
        compare(result, dummy)

class DummyModelAdmin(object):
    def __init__(self, name=None, model=None, schema=None):
        self.name = name
        self.model = model
        self.schema = schema
