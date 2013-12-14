from pyramid_layout.layout import layout_config


@layout_config(template="rebecca.app.admin:templates/base.mako")
class BaseLayout(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
