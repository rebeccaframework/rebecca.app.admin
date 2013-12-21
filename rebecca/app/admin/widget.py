from deform.widget import Widget
from colander import null
from webhelpers2.html import literal, escape


class RelationWidget(Widget):
    tmpl = ('<input type="text"'
            ' name="{values[field].name}"'
            ' value="{values[cstruct]}"'
            ' data-model="{values[model]}">')

    def serialize(self, field, cstruct, **kw):
        model = field.typ.model
        if cstruct == null:
            cstruct = ''
        kw = {'model': model.__name__.lower()}
        values = self.get_template_values(field, escape(cstruct), kw)
        return literal(self.tmpl).format(values=values)

    def deserialize(self, field, pstruct):
        pstruct = pstruct.strip()
        if not pstruct:
            return null
        return pstruct
