from pyramid.httpexceptions import HTTPFound, HTTPNotFound
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

    @view_config(name='search', renderer='json')
    def search(self):
        """ search specified path_info properties """
        if len(self.request.subpath) != 1:
            return HTTPNotFound()
        rel_name = self.request.subpath[0]
        rel_items = self.context.search_relation(rel_name)
        items = [(i.id, str(i)) for i in rel_items]  # TODO: inspect primary key
        return dict(rel_name=rel_name,
                    items=items)

    @view_config(name="new",
                 renderer="rebecca.app.admin:templates/new_model_form.mako")
    def new(self):
        """ create new model object """
        form = Form(self.context.schema, buttons=('add',))
        resources = form.get_widget_resources()
        js_resources = resources['js']
        css_resources = resources['css']
        js_links = [self.request.static_url(r) for r in js_resources]
        css_links = [self.request.static_url(r) for r in css_resources]
        js_tags = [literal('<script type="text/javascript" src="%s"></script>' % link)
                   for link in js_links]
        css_tags = [literal('<link rel="stylesheet" href="%s"/>' % link)
                    for link in css_links]
        resource_tags = js_tags + css_tags

        if self.request.method == 'POST':
            controls = self.request.params.items()
            try:
                params = form.validate(controls)
                item = self.context.add(params)
                del self.request.matchdict['traverse']
                location = self.request.resource_url(
                    self.context,
                    route_name=self.request.matched_route.name,
                    route_kw=self.request.matchdict)

                return HTTPFound(location=location)

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
