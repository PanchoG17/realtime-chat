from django.urls import path

from data_stream import consumers

websocket_urlpatterns = [
    path('chat/<str:room_name>', consumers.ChatConsumer.as_asgi())
]