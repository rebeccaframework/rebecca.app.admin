import logging
from zope.interface import implementer
from .interfaces import IModelAdmin, IAdminSite


logger = logging.getLogger(__name__)


@implementer(IAdminSite)
class AdminSite(object):
    __name__ = __parent__ = None

    def __init__(self, request):
        reg = request.registry
        self.request = request
        self.model_admins = dict(reg.getUtilitiesFor(IModelAdmin))

    def __iter__(self):
        return iter(self.model_admins)

    def __getitem__(self, key):
        model_admin = self.model_admins[key]
        return model_admin
