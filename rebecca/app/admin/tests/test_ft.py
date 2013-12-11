import unittest
import webtest


class FunctionalTest(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from pyramid.config import Configurator

        config = Configurator()
        config.include('rebecca.app.admin')
        config.add_admin_model('rebecca.app.admin.testing.Person')
        return config.make_wsgi_app()

    def test_it(self):
        app = self._makeOne()
        app = webtest.TestApp(app)
        res = app.get('/')
        self.assertIn('http://localhost/person', res)

        app.get('http://localhost/person')
