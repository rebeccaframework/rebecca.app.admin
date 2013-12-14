<a href="${request.resource_url(request.context, '@@new', route_name=request.matched_route.name, route_kw=request.matchdict)}">New</a>
<ul class="nav">
%for item in request.context.items():
<li><a href="${request.resource_url(request.context, item.id)}">${item}</a></li>
%endfor
</ul>