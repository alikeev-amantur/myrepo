import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from happyhours.factories import UserFactory, EstablishmentFactory
from ..models import Establishment


@pytest.mark.django_db
class TestEstablishmentAPI:
    client = APIClient()

    def test_create_establishment_api(self):
        user = UserFactory(role="partner")
        self.client.force_authenticate(user=user)
        url = reverse('v1:establishment-create')
        data = {
            'name': 'New Establishment',
            'description': 'A new sample establishment',
            'location': {
                'type': 'Point',
                'coordinates': [10, 20]
            },
            'owner': user.id
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Establishment.objects.count() == 1
        assert Establishment.objects.get().name == 'New Establishment'

    def test_retrieve_establishment_api(self):
        establishment = EstablishmentFactory()
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('v1:establishment-detail', kwargs={'pk': establishment.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_establishment_api(self):
        user = UserFactory()
        establishment = EstablishmentFactory(owner=user)
        self.client.force_authenticate(user=user)
        url = reverse('v1:establishment-detail', kwargs={'pk': establishment.pk})
        new_name = "Updated Name"
        response = self.client.patch(url, {'name': new_name}, format='json')
        assert response.status_code == status.HTTP_200_OK
        establishment.refresh_from_db()
        assert establishment.name == new_name

    def test_delete_establishment_api(self):
        user = UserFactory(role="admin")
        self.client.force_authenticate(user=user)
        establishment = EstablishmentFactory()
        url = reverse('v1:establishment-detail', kwargs={'pk': establishment.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Establishment.objects.count() == 0
