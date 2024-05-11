import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'happyhours.settings.local')
django.setup()
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.order import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'happyhours.settings.local')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
             routing.websocket_urlpatterns
        )
    ),
})
