from pyramid.config import Configurator

def main(global_conf, **settings):
    config = Configurator(settings=settings)
    config.add_admin_model('.models.Person')
    return config.make_wsgi_app()
