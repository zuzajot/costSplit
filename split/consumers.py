import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer


class CostConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            settings.TICKS_GROUP_NAME,
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave ticks group
        async_to_sync(self.channel_layer.group_discard)(
            settings.TICKS_GROUP_NAME,
            self.channel_name
        )

    def new_ticks(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })


class PaymentConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
