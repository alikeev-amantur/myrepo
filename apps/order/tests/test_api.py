import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from apps.order.models import Order
from happyhours.factories import (
    UserFactory,
    BeverageFactory,
    EstablishmentFactory,
    OrderFactory,
)


@pytest.mark.django_db
class TestOrderViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory(role="client")
        self.partner = UserFactory(role="partner")
        self.establishment = EstablishmentFactory(
            owner=self.partner, happyhours_start="01:00:00", happyhours_end="23:59:00"
        )
        self.beverage = BeverageFactory(establishment=self.establishment)
        self.order = OrderFactory(client=self.user, beverage=self.beverage)
        self.place_order_url = reverse("v1:place-order")
        self.client_order_history_url = reverse("v1:client-order-history-list")
        self.partner_order_history_url = reverse("v1:partner-order-history-list")

    def test_place_order_permissions(self):
        response = self.client.post(self.place_order_url, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        establishment = EstablishmentFactory(
            happyhours_start="00:00:00", happyhours_end="23:59:00"
        )
        beverage = BeverageFactory(establishment=establishment)
        user = UserFactory(role="client")
        self.client.force_authenticate(user=user)
        order_data = {"beverage": beverage.id}
        response = self.client.post(self.place_order_url, order_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["client"] == user.id
        assert response.data["establishment"] == beverage.establishment.id

    def test_client_order_history_permissions(self):
        response = self.client.get(self.client_order_history_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.client_order_history_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Order.objects.filter(client=self.user).count()

    def test_partner_order_history_permissions(self):
        response = self.client.get(self.partner_order_history_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        self.client.force_authenticate(user=self.partner)
        response = self.client.get(self.partner_order_history_url)
        assert response.status_code == status.HTTP_200_OK

    def test_partner_order_history_data(self):
        self.client.force_authenticate(user=self.partner)
        response = self.client.get(self.partner_order_history_url)
        assert (
            len(response.data)
            == Order.objects.filter(establishment__owner=self.partner).count()
        )
