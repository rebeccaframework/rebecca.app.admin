<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css"
	  href="${request.static_url('deform:static/css/bootstrap.min.css')}"/>
    <link rel="stylesheet" type="text/css"
	  href="${request.static_url('deform:static/css/form.css')}"/>
    <script src="${request.static_url('deform:static/scripts/jquery-2.0.3.min.js')}"></script>
    <script src="${request.static_url('deform:static/scripts/bootstrap.min.js')}"></script>
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
