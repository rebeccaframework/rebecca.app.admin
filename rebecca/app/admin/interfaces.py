from zope.interface import Interface, Attribute


class IModelAdminFactory(Interface):
    def __call__(parent):
        """ """


class IModelAdmin(Interface):
    """ administration to model """
    name = Attribute(u"name of function")
    model = Attribute(u"model to administrait")
    schema = Attribute(u"schema for model")

    def add(values):
        """ add new item """

class IAdminSite(Interface):
    """ admin tool site"""
