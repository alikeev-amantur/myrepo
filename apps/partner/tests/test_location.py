import pytest
from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APIClient

from apps.partner.models import Establishment
from happyhours.factories import EstablishmentFactory, UserFactory


@pytest.mark.django_db
class TestEstablishmentAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory(role='partner')
        self.client.force_authenticate(user=self.user)
        self.establishment_data = {
            "name": "Test Establishment",
            'location': {
                'type': 'Point',
                'coordinates': [10, 20]
            },
            "description": "A new establishment",
            "address": "1234 Test St."
        }

    def test_retrieve_establishment_with_location(self):
        establishment = EstablishmentFactory(
            owner=self.user,
            location=Point(10.0, 20.0)
        )

        # GET method
        response = self.client.get(f'/api/v1/partner/establishment/{establishment.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['coordinates'] == [10.0, 20.0]

    def test_create_establishment_with_valid_location(self):
        # POST method with valid data
        response = self.client.post('/api/v1/partner/establishment/create/', data=self.establishment_data,
                                    format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['location']['coordinates'] == [10.0, 20.0]
        assert Establishment.objects.count() == 1

    def test_create_establishment_with_invalid_location(self):
        # Invalid location data
        invalid_data = self.establishment_data.copy()
        invalid_data['location'] = {"type": "Point", "coordinates": [190.0, 95.0]}

        response = self.client.post('/api/v1/partner/establishment/create/', data=invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'location' in response.data
        assert Establishment.objects.count() == 0
