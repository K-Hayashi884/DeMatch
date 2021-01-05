# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Talk, User, Group, UserTalk, GroupTalk
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
                'user_id':self.user.id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        # user_id = self.user.id
        username = await self._save_message(message, user_id)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    # DB操作を伴う処理を含んだメソッド
    @database_sync_to_async
    def _save_message(self, text, user_id):
        talk_from = User.objects.get(id=user_id)
        talk_to = User.objects.get(id=self.room_name)
        new_talk = UserTalk(text=text, talk_from=talk_from, talk_to=talk_to, time=datetime.datetime.now(),)
        new_talk.save()
        return talk_from.username

class GroupChatConsumer(AsyncWebsocketConsumer):
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
                'user_id':self.user.id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        # user_id = self.user.id
        username = await self._save_message(message, user_id)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    # DB操作を伴う処理を含んだメソッド
    @database_sync_to_async
    def _save_message(self, text, user_id):
        talk_from = User.objects.get(id=user_id)
        talk_to = Group.objects.get(id=self.room_name)
        new_talk = GroupTalk(text=text, talk_from=talk_from, talk_to=talk_to, time=datetime.datetime.now(),)
        new_talk.save()
        return talk_from.username
