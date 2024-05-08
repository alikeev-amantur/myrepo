import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Establishment, Order


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.establishment_id = self.scope['url_route']['kwargs']['establishment_id']
        self.room_group_name = f'order_updates_{self.establishment_id}'
        self.user = self.scope["user"]

        if await self.is_establishment_owner(self.establishment_id, self.user):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        order_id = text_data_json['order_id']
        status = text_data_json['status']

        if await self.update_order_status(order_id, status):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_order_update',
                    'order_id': order_id,
                    'status': status
                }
            )

    async def send_order_update(self, event):
        await self.send(text_data=json.dumps({
            'order_id': event['order_id'],
            'status': event['status']
        }))

    @database_sync_to_async
    def is_establishment_owner(self, establishment_id, user):
        return Establishment.objects.filter(id=establishment_id, owner=user).exists()

    @database_sync_to_async
    def update_order_status(self, order_id, status):
        order = Order.objects.filter(id=order_id, establishment_id=self.establishment_id).first()
        if order:
            order.status = status
            order.save()
            return True
        return False
