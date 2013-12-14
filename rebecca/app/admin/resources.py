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
        self.model_admins = dict(reg.getAdapters((self,), IModelAdmin))
        logger.debug('admins {admins}'.format(admins=self.model_admins))

    def __iter__(self):
        return iter(self.model_admins)

    def __getitem__(self, key):
        logger.debug('traversal {key}'.format(key=key))
        model_admin = self.model_admins[key]
        logger.debug('{key} {resource}'.format(key=key,
                                               resource=model_admin))
        return model_admin
