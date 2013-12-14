from pyramid.view import view_config, view_defaults


@view_defaults(route_name="rebecca.admin.site",
               context='.interfaces.IModelAdmin')
class ModelAdminView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(renderer="rebecca.app.admin:templates/index_models.mako")
    def index(self):
        """ show grid of members"""
        return dict()

    def search(self):
        """ search specified path_info properties """


@view_defaults(route_name="rebecca.admin.site",
               context='.interfaces.IAdminSite')
class AdminSiteView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(renderer="rebecca.app.admin:templates/index.mako")
    def index(self):
        """ show model admin menus """
        return dict()
