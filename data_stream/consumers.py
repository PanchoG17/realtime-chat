from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'You are connected!'
        }))


    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )


    def chat_message(self, event):
        message = event['message']
        user = self.scope['user']
        self.send(text_data=json.dumps({
            'type':'chat',
            'message': f'{user}: {message}'
        }))


    def disconnect(self, close_code):
        pass
