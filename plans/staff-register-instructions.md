# Register Staff Routes in API/__init__.py

Add after companies delete_company import (line24):

```
from API.routes.staff.qr import QrRoute
from API.routes.staff.get_user_by_access_token import GetUserByAccessTokenRoute
from API.routes.staff.retrieve_connections import RetrieveConnectionsRoute
from API.routes.staff.add_connection import AddConnectionRoute
```

After delete_company_route = (line60):

```
qr_route = QrRoute()
get_user_by_access_token_route = GetUserByAccessTokenRoute()
retrieve_connections_route = RetrieveConnectionsRoute()
add_connection_route = AddConnectionRoute()
```

After app.register_blueprint(delete_company_route.bp...) (line84):

```
app.register_blueprint(qr_route.bp, url_prefix="/api/v1")
app.register_blueprint(get_user_by_access_token_route.bp, url_prefix="/api/v1")
app.register_blueprint(retrieve_connections_route.bp, url_prefix="/api/v1")
app.register_blueprint(add_connection_route.bp, url_prefix="/api/v1")
```

Restart app.