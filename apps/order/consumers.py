import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Order
from .utils import get_user_from_token
from django.contrib.auth.models import AnonymousUser

from ..partner.models import Establishment


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('token=')[1] if 'token=' in self.scope[
            'query_string'].decode() else None
        user = await database_sync_to_async(get_user_from_token)(token)

        if not user or user.is_anonymous or user.role != 'partner':
            await self.close()
        else:
            self.user = user

            establishment_id = self.scope['url_route']['kwargs']['establishment_id']
            establishment = await database_sync_to_async(self.get_establishment)(establishment_id)

            if establishment and establishment.owner_id == self.user.id:
                self.room_group_name = f'order_{establishment_id}'

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()
            else:
                await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        order_id = text_data_json['order_id']
        new_status = text_data_json['status']

        await self.update_order_status(order_id, new_status)

    async def order_message(self, event):
        await self.send(text_data=json.dumps({
            'order_id': event['order_id'],
            'establishment_id': event['establishment_id'],
            'status': event['status'],
            'details': event['details']
        }))

    @database_sync_to_async
    def update_order_status(self, order_id, new_status):
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return True
        except Order.DoesNotExist:
            return False

    @database_sync_to_async
    def get_establishment(self, establishment_id):
        try:
            return Establishment.objects.get(id=establishment_id)
        except Establishment.DoesNotExist:
            return None
