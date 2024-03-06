from django.urls import path
from data_stream import views

urlpatterns = [
    path('', views.lobby),
]