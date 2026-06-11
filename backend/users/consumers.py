import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.gis.geos import Point


class GPSTrackingConsumer(AsyncWebsocketConsumer):
    """Suivi GPS temps réel des équipes de secours."""

    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add("gps_tracking", self.channel_name)
        if hasattr(user, "role") and user.role == "rescue":
            await self.channel_layer.group_add("rescue_gps", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gps_tracking", self.channel_name)
        user = self.scope.get("user")
        if user and hasattr(user, "role") and user.role == "rescue":
            await self.channel_layer.group_discard("rescue_gps", self.channel_name)

    async def receive(self, text_data):
        user = self.scope["user"]
        if not hasattr(user, "role") or user.role != "rescue":
            return

        data = json.loads(text_data)
        lat = data.get("lat")
        lng = data.get("lng")
        if lat is None or lng is None:
            return

        await self._update_position(user.id, float(lat), float(lng))
        payload = {
            "type": "gps_update",
            "user_id": user.id,
            "username": user.username,
            "name": user.get_full_name() or user.username,
            "lat": lat,
            "lng": lng,
            "is_available": user.is_available,
        }
        await self.channel_layer.group_send("gps_tracking", {
            "type": "gps_broadcast",
            "data": payload,
        })

    async def gps_broadcast(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    @database_sync_to_async
    def _update_position(self, user_id, lat, lng):
        from users.models import User
        User.objects.filter(id=user_id).update(last_position=Point(lng, lat, srid=4326))
