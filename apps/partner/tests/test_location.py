import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock
from apps.partner.models import Establishment
from happyhours.factories import EstablishmentFactory, UserFactory


@pytest.mark.django_db
class TestEstablishmentAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory(role="partner")
        self.client.force_authenticate(user=self.user)
        self.establishment_data = {
            "name": "Test Establishment",
            "location": {"type": "Point", "coordinates": [10, 20]},
            "description": "A new establishment",
            "address": "1234 Test St.",
        }

    def test_retrieve_establishment_with_location(self):
        establishment = EstablishmentFactory(
            owner=self.user, location=Point(10.0, 20.0)
        )
        response = self.client.get(f"/api/v1/partner/establishment/{establishment.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["location"]["coordinates"] == [10.0, 20.0]

    def test_create_establishment_with_valid_location(self):
        response = self.client.post(
            "/api/v1/partner/establishments/",
            data=self.establishment_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["location"]["coordinates"] == [10.0, 20.0]
        assert Establishment.objects.count() == 1

    def test_create_establishment_with_invalid_location(self):
        invalid_data = self.establishment_data.copy()
        invalid_data["location"] = {"type": "Point", "coordinates": [190.0, 95.0]}

        response = self.client.post(
            "/api/v1/partner/establishments/", data=invalid_data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "location" in response.data
        assert Establishment.objects.count() == 0


@pytest.mark.django_db
class TestEstablishmentLocationView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("v1:establishments")
        self.user = UserFactory(role="client")
        self.establishment1 = EstablishmentFactory(
            location=Point(74.61662756863511, 42.82463980484438, srid=4326),
            happyhours_start=timezone.now().replace(hour=9, minute=0),
            happyhours_end=timezone.now().replace(hour=11, minute=0),
        )
        self.establishment2 = EstablishmentFactory(
            location=Point(10, 20, srid=4326),
            happyhours_start=timezone.now().replace(hour=15, minute=0),
            happyhours_end=timezone.now().replace(hour=17, minute=0),
        )

    def test_filter_by_distance(self):
        params = {
            "latitude": "42.82463980484438",
            "longitude": "74.61651510051765",
            "near_me": "50000",
        }
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, params)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == self.establishment1.id

    def test_filter_happyhours_active(self):
        current_time = timezone.now().replace(hour=10, minute=0)
        with mock.patch("django.utils.timezone.localtime", return_value=current_time):
            params = {"happyhours_active": "true"}
            self.client.force_authenticate(self.user)
            response = self.client.get(self.url, params)
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data) == 1
            assert response.data[0]["id"] == self.establishment1.id
