from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync
import json

from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):


    ## Connection
    def connect(self):

        # Get the user agent from headers
        user_agent_tuple = next((item for item in self.scope['headers'] if item[0] == b'user-agent'), None)
        user_agent_value = user_agent_tuple[1].decode('utf-8')

        browsers_list = ["Mozilla", "AppleWebKit", "Chrome"]
        if any(x in user_agent_value for x in browsers_list):
            agent = 'Browser client'

        elif ('Python' in user_agent_value):
            agent = 'Python CLI client'

        # Get the user name from headers or scope
        user_name_tuple = next((item for item in self.scope['headers'] if item[0] == b'user'), None)
        user_name_value = user_name_tuple[1].decode('utf-8') if user_name_tuple else None
        self.user = self.scope['user'].username or user_name_value or 'Anonymous user'

        # Get room name from URL param
        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{room_name}'
    
        # Connect to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        # Send back response
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'user_connected',
                'user':self.user,
                'agent':agent
            }
        )


    ## Manage incoming messages
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
        agent = event['agent']
        self.send(text_data=json.dumps({
            'type':'user_connected',
            'message': f'## {user} enter to the chatroom ##',
            'agent':agent
        }))


    def disconnect(self, close_code):
        pass
