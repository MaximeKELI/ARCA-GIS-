import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.incident_id = self.scope["url_route"]["kwargs"]["incident_id"]
        self.room = f"chat_{self.incident_id}"
        user = self.scope.get("user")

        if not user or not user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive(self, text_data):
        user = self.scope["user"]
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        if not message:
            return

        msg = await self._save_message(int(self.incident_id), user.id, message)
        await self.channel_layer.group_send(self.room, {
            "type": "chat_message",
            "message": {
                "id": msg.id,
                "sender": user.username,
                "sender_name": user.get_full_name() or user.username,
                "sender_role": user.role,
                "message": message,
                "created_at": msg.created_at.isoformat(),
            },
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def _save_message(self, incident_id, user_id, message):
        from users.models import User
        return ChatMessage.objects.create(
            incident_id=incident_id,
            sender_id=user_id,
            message=message,
        )
