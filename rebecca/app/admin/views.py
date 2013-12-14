from pyramid.view import view_config, view_defaults
from webhelpers2.html import HTML, escape, literal
from deform import ValidationFailure
from deform.form import Form

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


    @view_config(name="new",
                 renderer="rebecca.app.admin:templates/new_model_form.mako")
    def new(self):
        """ create new model object """
        form = Form(self.context.schema, buttons=('add',))
        resources = form.get_widget_resources()
        js_resources = resources['js']
        css_resources = resources['css']
        js_links = [self.request.static_url(r) for r in js_resources ]
        css_links = [self.request.static_url(r) for r in css_resources ]
        js_tags = [literal('<script type="text/javascript" src="%s"></script>' % link)
                   for link in js_links]
        css_tags = [literal('<link rel="stylesheet" href="%s"/>' % link)
                    for link in css_links]
        resource_tags = js_tags + css_tags

        if self.request.method == 'POST':
            controls = self.request.params.items()
            try:
                form.validate(controls)
            except ValidationFailure as e:
                return dict(form=e.render(), resource_tags=resource_tags)
        return dict(form=form.render(), resource_tags=resource_tags)


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
