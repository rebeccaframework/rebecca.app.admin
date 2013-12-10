from zope.interface import Interface, Attribute


class IModelAdmin(Interface):
    """ administration to model """
    name = Attribute(u"name of function")
    model = Attribute(u"model to administrait")
    schema = Attribute(u"schema for model")
