<%inherit file="${context['main_template'].uri}"/>

<ul class="nav">
%for item in request.context:
<li><a href="${request.resource_url(request.context, item, route_name=request.matched_route.name, route_kw=request.matchdict)}">${item}</a>
%endfor
</ul>