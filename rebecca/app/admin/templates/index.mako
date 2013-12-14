<%inherit file="${context['main_template'].uri}"/>

%for category in request.context.categories:
<div class="panel panel-default">
  <div class="panel-heading">
    <h2 class="panel-title">${category}</h2>
  </div>
  <div class="panel-body">
    <ul class="nav">
      %for item in request.context.get_categoried_admins(category):
      <li>
	<a href="${request.resource_url(request.context, item.name, route_name=request.matched_route.name, route_kw=request.matchdict)}">
	  ${item.name}
	</a>
      </li>
      %endfor
    </ul>
  </div>
</div>
%endfor

