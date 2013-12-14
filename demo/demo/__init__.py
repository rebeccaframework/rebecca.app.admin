from pyramid.config import Configurator
from sqlalchemy import engine_from_config

def main(global_conf, **settings):
    engine = engine_from_config(settings)
    from . import models
    models.init(engine)

    config = Configurator(settings=settings)
    config.add_admin_model('.models.Person')
    return config.make_wsgi_app()
