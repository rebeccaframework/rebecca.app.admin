<ul class="nav">
%for item in request.context:
<li><a href="${request.resource_url(request.context, item)}">${item}</a>
%endfor
</ul>