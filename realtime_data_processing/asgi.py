"""
ASGI config for realtime_data_processing project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import data_stream.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_data_processing.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            data_stream.routing.websocket_urlpatterns
        )
    )
})
