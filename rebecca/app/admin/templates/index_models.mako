<ul class="nav">
%for item in request.context.items():
<li><a href="#">${item}</a></li>
%endfor
</ul>