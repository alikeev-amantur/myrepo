from unittest.mock import MagicMock

import pytest
from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError

from happyhours.factories import EstablishmentFactory, UserFactory
from ..serializers import EstablishmentCreateUpdateSerializer, EstablishmentSerializer


@pytest.mark.django_db
class TestEstablishmentSerializer:
    def test_representation_includes_logo_url(self):
        establishment = EstablishmentFactory()
        serializer = EstablishmentSerializer(establishment)
        expected_logo_url = serializer.get_image_url(establishment)

        data = serializer.data
        assert data['logo'] == expected_logo_url

    def test_validate_location_valid(self):
        serializer = EstablishmentCreateUpdateSerializer()
        valid_location = Point(10, 20)
        assert serializer.validate_location(valid_location) == valid_location

    def test_validate_location_invalid_type(self):
        serializer = EstablishmentCreateUpdateSerializer()
        with pytest.raises(ValidationError):
            serializer.validate_location("NotAPointObject")

    def test_validate_location_out_of_bounds(self):
        serializer = EstablishmentCreateUpdateSerializer()
        out_of_bounds_location = Point(-200, 100)
        with pytest.raises(ValidationError):
            serializer.validate_location(out_of_bounds_location)


    def test_validate_owner_incorrect(self):
        user = UserFactory()
        other_user = UserFactory()
        serializer = EstablishmentCreateUpdateSerializer(context={'request': MagicMock(user=user)})
        with pytest.raises(ValidationError):
            serializer.validate_owner(other_user)

    def test_create_establishment(self):
        user = UserFactory()
        data = {
            'name': 'New Establishment',
            'location': Point(10, 20),
            'description': 'A place for everyone.',
            'owner': user.id,
        }
        serializer = EstablishmentCreateUpdateSerializer(data=data, context={'request': MagicMock(user=user)})
        if serializer.is_valid():
            establishment = serializer.save()
            assert establishment.name == data['name']
            assert establishment.owner == user
        else:
            pytest.fail(f"Serializer errors: {serializer.errors}")


@pytest.fixture
def phone_number_validation(mocker):
    mocker.patch('path.to.phone_number_validation', return_value=True)
