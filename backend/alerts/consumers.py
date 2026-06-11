import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add("alerts", self.channel_name)

        if hasattr(user, "role"):
            await self.channel_layer.group_add(f"role_{user.role}", self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connecté au flux d'alertes ARCA-GIS",
            "user": user.username,
            "role": user.role,
        }))

    async def disconnect(self, close_code):
        user = self.scope.get("user")
        if user and user.is_authenticated:
            await self.channel_layer.group_discard("alerts", self.channel_name)
            if hasattr(user, "role"):
                await self.channel_layer.group_discard(f"role_{user.role}", self.channel_name)

    async def alert_message(self, event):
        await self.send(text_data=json.dumps(event["alert"]))
