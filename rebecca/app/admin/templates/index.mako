${request.current_route_url()}
<ul class="nav">
%for item in request.context:
<li><a href="${request.resource_url(request.context, item, route=request.matched_route.name, route_kw=request.matchdict)}">${item}</a>
%endfor
</ul>