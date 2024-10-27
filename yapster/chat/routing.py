from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/<str:chat_name>/', ChatConsumer.as_asgi()),
]