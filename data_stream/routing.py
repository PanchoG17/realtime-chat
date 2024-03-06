from django.urls import re_path

from data_stream import consumers

websocket_urlpatterns = [
    re_path(r'ws/echo/', consumers.ChatConsumer.as_asgi())
]