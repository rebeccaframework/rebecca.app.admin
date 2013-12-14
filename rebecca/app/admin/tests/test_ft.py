import unittest
import webtest


class FunctionalTest(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from pyramid.config import Configurator
        from rebecca.app.admin.testing import DBSession, Base
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///')
        Base.metadata.create_all(bind=engine)
        DBSession.configure(bind=engine)

        config = Configurator()
        config.include('rebecca.app.admin')
        config.add_admin_model(
            'rebecca.app.admin.testing.Person',
            sessionmaker='rebecca.app.admin.testing.DBSession')
        return config.make_wsgi_app()

    def test_it(self):
        app = self._makeOne()
        app = webtest.TestApp(app)
        res = app.get('/')
        self.assertIn('http://localhost/person', res)

        app.get('http://localhost/person')
