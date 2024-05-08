"""
ASGI config for happyhours project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django_channels_jwt.middleware import JwtAuthMiddlewareStack

from apps.order import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "happyhours.settings.local")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
