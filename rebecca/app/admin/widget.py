from deform.widget import Widget
from colander import null


class RelationWidget(Widget):
    url = ""
    template = 'relation'

    def serialize(self, field, cstruct, **kw):
        model = field.typ.model
        if cstruct == null:
            cstruct = ''
        kw = {'model': model.__name__.lower(),
              'url': self.url}
        values = self.get_template_values(field, cstruct, kw)
        return field.renderer(self.template, **values)

    def deserialize(self, field, pstruct):
        pstruct = pstruct.strip()
        if not pstruct:
            return null
        return pstruct
