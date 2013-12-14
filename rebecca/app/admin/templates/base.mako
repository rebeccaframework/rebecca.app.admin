<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css"
	  href="${request.static_url('deform:static/css/bootstrap.min.css')}"/>
    <link rel="stylesheet" type="text/css"
	  href="${request.static_url('deform:static/css/form.css')}"/>
    <script src="${request.static_url('deform:static/scripts/jquery-2.0.3.min.js')}"></script>
    <script src="${request.static_url('deform:static/scripts/bootstrap.min.js')}"></script>
    <%block name="additional_headers"></%block>
  </head>
  <body>
    <nav class="navbar navbar-default" role="navigation">
      <div class="collapse navbar-collapse">
	<ul class="nav navbar-nav">
	  <li><a href="${request.resource_url(request.root, route_name=request.matched_route.name)}">TOP</a>
	</ul>
      </div>
    </nav>
    <div class="container">
    ${next.body()}
    </div>
  </body>
</html>
