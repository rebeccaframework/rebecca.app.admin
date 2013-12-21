# -*- coding:utf-8 -*-

from pyramid.config import Configurator
from sqlalchemy import engine_from_config


def main(global_conf, **settings):
    engine = engine_from_config(settings)
    from . import models
    models.init(engine)

    config = Configurator(settings=settings)
    config.include('rebecca.app.admin',
                   route_prefix='/admin')
    config.add_admin_model('.models.Person',
                           '.models.DBSession')
    config.add_admin_model('.models.Job',
                           '.models.DBSession',
                           category=u'カテゴリ1')
    config.add_admin_model('.models.Company',
                           '.models.DBSession',
                           category=u'カテゴリ1')
    return config.make_wsgi_app()
