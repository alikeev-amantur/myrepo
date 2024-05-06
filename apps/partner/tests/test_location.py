import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

from happyhours.factories import UserFactory
from ..models import Establishment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_establishment(db, test_user):
    return Establishment.objects.create(
        name="Test Bar",
        location=Point(34.052235, -118.243683),
        owner=test_user
    )


# @pytest.mark.django_db
# def test_establishment_serializer_create(api_client, test_user):
#     api_client.force_authenticate(user=test_user)
#     data = {
#         "name": "New Bar",
#         "location": {"type": "Point", "coordinates": [-118.243683, 34.052235]},
#         "owner": test_user.id
#     }
#     response = api_client.post('/api/establishments/', data, format='json')
#     assert response.status_code == 201
#     assert response.data['location']['coordinates'] == [-118.243683, 34.052235]
#
#
# @pytest.mark.django_db
# def test_establishment_serializer_get(api_client, test_establishment):
#     api_client.force_authenticate(user=test_establishment.owner)
#     response = api_client.get(f'/api/establishments/{test_establishment.id}/')
#     assert response.status_code == 200
#     assert response.data['location']['coordinates'] == [34.052235, -118.243683]
