from pkg_resources import resource_filename
from deform import Form


def init_templates(config):
    deform_templates = resource_filename('deform', 'templates')
    rebecca_templates = resource_filename('rebecca.app.admin', 'widget_templates')
    search_path = (rebecca_templates, deform_templates)

    Form.set_zpt_renderer(search_path)


def includeme(config):
    config.include('pyramid_mako')
    config.include('pyramid_layout')
    config.add_static_view('deform-static', 'deform:static')
    config.add_route('rebecca.admin.site', '/*traverse',
                     factory=".resources.AdminSite")
    config.add_directive('add_admin_model',
                         '.config.add_admin_model')
    config.scan('.views')
    config.scan('.layouts')

    init_templates(config)
