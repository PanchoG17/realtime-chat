from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync
import json

from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{room_name}'
        self.user = self.scope['user'].username or 'Anonymus user'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'user_connected',
                'user': self.user
            }
        )


    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = data['user']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'user':user
            }
        )


    # Send message to chat room
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        
        self.send(text_data=json.dumps({
            'type':'chat',
            'message': f'{user}: {message}'
        }))


    # User connection notification
    def user_connected(self, event):
        user = event['user']
        self.send(text_data=json.dumps({
            'type':'user_connected',
            'message': f'{user} enter to the chatroom'
        }))


    def disconnect(self, close_code):
        pass
