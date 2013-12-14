<ul class="nav">
%for item in request.context.items():
<li><a href="${request.resource_url(request.context, item.id)}">${item}</a></li>
%endfor
</ul>