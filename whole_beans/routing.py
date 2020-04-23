from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

# protocolTypeRouter determmines if http or websocket request
# if http, follow url.py
# if websocket, use authMiddlewareStack to add to scope
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            # figure out what to do by follwing instructions found here.
            chat.routing.websocket_urlpatterns
        )
    ),
})

