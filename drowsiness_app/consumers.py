import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Alert


class MonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user != AnonymousUser():
            await self.accept()
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user != AnonymousUser():
            await self.channel_layer.group_discard(
                f"user_{self.user.id}", self.channel_name
            )

    async def send_message(self, event):
        await self.send(text_data=json.dumps(event))
