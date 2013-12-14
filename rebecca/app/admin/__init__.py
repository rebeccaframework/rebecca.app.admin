def includeme(config):
    config.include('pyramid_mako')
    config.add_static_view('deform-static', 'deform:static')
    config.add_route('rebecca.admin.site', '/*traverse',
                     factory=".resources.AdminSite")
    config.add_directive('add_admin_model',
                         '.config.add_admin_model')
    config.scan('.views')
