from django.urls import path
from data_stream import views

app_name="data_stream"

urlpatterns = [
    path('', views.lobby),
    path('chat/<str:room_name>', views.chat_room, name="chat_room"),
]