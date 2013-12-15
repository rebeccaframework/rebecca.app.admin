import unittest
import webtest


class FunctionalTest(unittest.TestCase):
    def _makeOne(self, *args, **kwargs):
        from pyramid.config import Configurator
        from rebecca.app.admin.testing import DBSession, Base
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///')
        Base.metadata.create_all(bind=engine)
        DBSession.remove()
        DBSession.configure(bind=engine)

        config = Configurator()
        config.include('rebecca.app.admin')
        config.add_admin_model(
            'rebecca.app.admin.testing.Person',
            sessionmaker='rebecca.app.admin.testing.DBSession')
        config.add_admin_model(
            'rebecca.app.admin.testing.Employee',
            sessionmaker='rebecca.app.admin.testing.DBSession')
        config.add_admin_model(
            'rebecca.app.admin.testing.Job',
            sessionmaker='rebecca.app.admin.testing.DBSession')
        return config.make_wsgi_app()

    def test_new_form(self):
        app = self._makeOne()
        app = webtest.TestApp(app)
        res = app.get('/')
        self.assertIn('http://localhost/person', res)

        app.get('http://localhost/person')
        res = app.get('http://localhost/person/@@new')
        res.form['first_name'] = 'testing'
        res.form['last_name'] = 'testing'
        res.form['birthday'] = '1070-01-01'
        res = res.form.submit('add')
        if not res.location:
            print(res)
        self.assertEqual(res.location,
                         'http://localhost//person/')  # it's strange
        res = app.get(res.location)

    def test_relation_search(self):
        app = self._makeOne()
        app = webtest.TestApp(app)
        res = app.get('/')
        self.assertIn('http://localhost/employee', res)
        res = app.get('/employee/@@search/job/aaa', status=404)
        res = app.get('/employee/@@search/job')
        self.assertEqual(res.json,
                         {
                             'rel_name': 'job',
                             'items': [],
                         })
        # register new job
        res = app.get('/job/@@new')
        res.form['name'] = 'new job'
        res.form.submit('add')

        res = app.get('/employee/@@search/job')
        self.assertEqual(res.json['rel_name'], 'job')
        self.assertEqual(res.json['items'],
                         [[1, 'Job id=1 name=new job']])
