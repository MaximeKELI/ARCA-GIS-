import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope["url_route"]["kwargs"]["auction_id"]
        self.group = f"auction_{self.auction_id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def auction_bid(self, event):
        await self.send(text_data=json.dumps({
            "type": "bid", "amount": event["amount"], "bidder": event["bidder"],
        }))
