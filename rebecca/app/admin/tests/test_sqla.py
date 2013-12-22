import unittest
from testfixtures import compare, Comparison as C


class TestDefaultTypeMapper(unittest.TestCase):

    def _getTarget(self):
        from ..sqla import DefaultTypeMapper
        return DefaultTypeMapper

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_it(self):
        target = self._makeOne()

    def test_boolean(self):
        from sqlalchemy.types import Boolean
        from sqlalchemy import Column
        import colander as c
        target = self._makeOne()
        result = target(Column('testing', Boolean()))

        compare(result.typ,
                C(c.Boolean()))

    def test_string(self):
        from sqlalchemy.types import String
        from sqlalchemy import Column
        import colander as c
        target = self._makeOne()
        result = target(Column('testing', String()))

        compare(result.typ,
                C(c.String()))

    def test_string_has_length(self):
        from sqlalchemy.types import String
        from sqlalchemy import Column
        import colander as c
        target = self._makeOne()
        result = target(Column('testing', String(10)))

        compare(result.typ,
                C(c.String))
        compare(result.validator,
                C(c.Length,
                  max=10,
                  min=0))

    def test_unicode(self):
        from sqlalchemy.types import Unicode
        from sqlalchemy import Column
        import colander as c
        target = self._makeOne()
        result = target(Column('testing', Unicode))

        compare(result.typ,
                C(c.String))

    def test_integer(self):
        from sqlalchemy.types import Integer
        from sqlalchemy import Column
        import colander as c
        target = self._makeOne()
        result = target(Column('testing', Integer()))

        compare(result.typ,
                C(c.Integer))

    def test_datetime(self):
        from sqlalchemy.types import DateTime
        from sqlalchemy import Column
        import colander as c
        target = self._makeOne()
        result = target(Column('testing', DateTime()))

        compare(result.typ,
                C(c.DateTime))


class Testget_related_model_mapper(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from ..sqla import get_related_model_mapper
        return get_related_model_mapper(*args, **kwargs)

    def test_it(self):
        from ..testing import Employee, Job
        result = self._callFUT(Employee, 'job')

        compare(result.class_, Job)


class Testquery_relation(unittest.TestCase):
    def setUp(self):
        from ..testing import _setup
        _setup()

    def tearDown(self):
        from ..testing import _teardown
        _teardown()

    def _callFUT(self, *args, **kwargs):
        from ..sqla import query_relation
        return query_relation(*args, **kwargs)

    def test_it(self):
        from ..testing import DBSession, Employee, Job
        job = Job()
        DBSession.add(job)
        DBSession.flush()
        result = self._callFUT(DBSession, Employee, 'job')
        jobs = list(result)
        compare(jobs, [job])


class Testcreate_schema(unittest.TestCase):

    def _callFUT(self, *args, **kwargs):
        from ..sqla import create_schema
        return create_schema(*args, **kwargs)

    def test_many_to_one(self):
        import colander
        from ..testing import DummyChild
        from ..schema import Relation
        result = self._callFUT(DummyChild)

        self.assertIn('name', result)
        self.assertNotIn('dummy_id', result)
        self.assertIn('dummy', result)
        compare(result['dummy'].typ,
                C(colander.deferred))
        deferred = result['dummy'].bind(db_session=object())
        compare(deferred.typ,
                C(Relation))

    # def test_one_to_many(self):
    #     from ..testing import DummySQLAModel
    #     from ..schema import Relation
    #     result = self._callFUT(DummySQLAModel)

    #     self.assertIn('value', result)
    #     self.assertIn('children', result)
    #     compare(result['children'].typ,
    #             C(Relation))
