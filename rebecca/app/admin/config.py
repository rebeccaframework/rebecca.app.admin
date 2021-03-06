""" config directives
"""
from .sqla import SQLAModelAdminFactory
from .interfaces import IAdminSite, IModelAdmin


reg_prefix = 'rebecca.admin.'
def add_admin_model(config, model, sessionmaker, name=None, category=None):
    """ add model to admin
    """
    model = config.maybe_dotted(model)
    model_name = model.__name__.lower()
    if category is None:
        category =model.__module__
    sessionmaker = config.maybe_dotted(sessionmaker)

    if name is None:
        name = model_name
    reg = config.registry
    def register():
        model_admin = SQLAModelAdminFactory(
            name=name,
            sessionmaker=sessionmaker,
            model=model,
            category=category)
        reg.registerAdapter(model_admin,
                            [IAdminSite],
                            IModelAdmin,
                            name=name)

    reg_name = reg_prefix + name

    config.action(reg_name, register)
