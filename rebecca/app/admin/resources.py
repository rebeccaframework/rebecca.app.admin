from .interfaces import IModelAdmin


class AdminSite(object):

    def __init__(self, request):
        reg = request.registry
        self.request = request
        self.model_admins = dict(reg.getUtilitiesFor(IModelAdmin))

    def __iter__(self):
        return iter(self.model_admins)

    def __getitem__(self, key):
        return self.model_admins[key]
