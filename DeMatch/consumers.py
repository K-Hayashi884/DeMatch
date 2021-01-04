# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Talk, User
import datetime
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'DeMatch_%s' % self.room_name
        self.user = self.scope['user']
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = self.user.id
        await self._save_message(message)
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id':user_id,
        }))

    # DB操作を伴う処理を含んだメソッド
    @database_sync_to_async
    def _save_message(self, text):
        talk_from = self.user
        talk_to = User.objects.get(id=self.room_name)
        new_talk = Talk(text=text, talk_from=talk_from, talk_to=talk_to, time=datetime.datetime.now(),)
        new_talk.save()
