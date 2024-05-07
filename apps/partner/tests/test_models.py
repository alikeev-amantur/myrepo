import pytest
from django.contrib.auth import get_user_model
from happyhours.factories import EstablishmentFactory
from ..models import Establishment

User = get_user_model()


@pytest.mark.django_db
class TestEstablishmentModel:
    def test_establishment_creation(self):
        establishment = EstablishmentFactory(name="Me")
        assert establishment.name == "Me"
        assert isinstance(establishment.owner, User)
        assert str(establishment) == f"Establishment: {establishment.name}"

    def test_establishment_update(self):
        establishment = EstablishmentFactory()
        establishment.name = "Updated Name"
        establishment.save()
        updated = Establishment.objects.get(id=establishment.id)
        assert updated.name == "Updated Name"
