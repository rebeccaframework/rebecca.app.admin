""" config directives
"""
from .sqla import SQLAModelAdmin

reg_prefix = 'rebecca.admin.'
def add_admin_model(config, model, sessionmaker, name=None):
    """ add model to admin
    """
    model = config.maybe_dotted(model)
    model_name = model.__name__.lower()
    sessionmaker = config.maybe_dotted(sessionmaker)

    if name is None:
        name = model_name
    reg = config.registry
    def register():
        model_admin = SQLAModelAdmin(name=name,
                                     sessionmaker=sessionmaker,
                                     model=model)
        reg.registerUtility(model_admin,
                            name=name)

    reg_name = reg_prefix + name

    config.action(reg_name, register)
