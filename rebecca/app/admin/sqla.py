import colander as c
from zope.interface import implementer
from .interfaces import IModelAdmin

@implementer(IModelAdmin)
class SQLAModelAdmin(object):

    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.schema = c.MappingSchema()
