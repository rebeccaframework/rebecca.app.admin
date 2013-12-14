<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css"
	  href="${request.static_url('deform:static/css/bootstrap.min.css')}"/>
    <link rel="stylesheet" type="text/css"
	  href="${request.static_url('deform:static/css/form.css')}"/>
    %for t in resource_tags:
    ${t}
    %endfor
  </head>
  <body>
    <div class="container">
      ${form|n}
    </div>
  </body>
</html>
