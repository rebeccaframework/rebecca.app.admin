""" config directives
"""
from .sqla import SQLAModelAdmin

reg_prefix = 'rebecca.admin.'
def add_admin_model(config, model, name=None):
    """ add model to admin
    """
    model_name = model.__name__
    if name is None:
        name = model_name
    reg = config.registry
    def register():
        admin = SQLAModelAdmin(name=name,
                           model=model)
        reg.registerUtility(admin,
                            name=name)

    reg_name = reg_prefix + name

    config.action(reg_name, register)
