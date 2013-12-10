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

