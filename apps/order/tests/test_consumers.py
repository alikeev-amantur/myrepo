import pytest
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken

from ..consumers import OrderConsumer
from happyhours.factories import UserFactory, EstablishmentFactory, OrderFactory

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
async def setup_data():
    client = await database_sync_to_async(UserFactory)(role='client')
    owner = await database_sync_to_async(UserFactory)(role='partner')
    establishment = await database_sync_to_async(EstablishmentFactory)(owner=owner)
    order = await database_sync_to_async(OrderFactory)(establishment=establishment, client=client)
    tokens = await database_sync_to_async(get_tokens_for_user)(owner)
    return client, owner, establishment, order, tokens


@pytest.mark.django_db
@pytest.mark.asyncio
class TestOrderConsumerJwtAuth:
    async def setup_communicator(self, establishment_id, token):
        application = URLRouter([
            path(f'ws/orders/{establishment_id}/', OrderConsumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, f'/ws/orders/{establishment_id}/?token={token}')
        connected, _ = await communicator.connect()
        return communicator, connected

    async def test_successful_connection(self, setup_data):
        _, owner, establishment, _, tokens = await setup_data
        communicator, connected = await self.setup_communicator(establishment.id, tokens['access'])
        assert connected, "Connection should be successful for valid token and role"
        await communicator.disconnect()

    async def test_order_update(self, setup_data):
        _, owner, establishment, order, tokens = await setup_data
        communicator, connected = await self.setup_communicator(establishment.id, tokens['access'])
        assert connected, "Connection should be successful for valid token"

        new_status = 'completed'
        await communicator.send_json_to({
            'order_id': order.id,
            'new_status': new_status
        })
        response = await communicator.receive_json_from()
        assert response == {
            'order_id': order.id,
            'establishment_id': establishment.id,
            'status': new_status,
            'details': 'Status updated'
        }, "Response should reflect the new order status"
        await communicator.disconnect()

    async def test_unauthorized_connection(self, setup_data):
        _, _, establishment, _, _ = await setup_data
        communicator, connected = await self.setup_communicator(establishment.id, 'invalid_token')
        assert not connected, "Connection should fail for invalid token"
        await communicator.disconnect()