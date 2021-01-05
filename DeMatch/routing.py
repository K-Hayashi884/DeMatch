# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/DeMatch/User/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/DeMatch/Group/(?P<room_name>\w+)/$', consumers.GroupChatConsumer.as_asgi()),
]