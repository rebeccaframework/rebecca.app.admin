<%inherit file="${context['main_template'].uri}"/>

<%block name="additional_headers">
%for t in resource_tags:
${t}
%endfor
</%block>

<div class="container">
  ${form|n}
</div>

