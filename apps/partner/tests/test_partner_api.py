import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from happyhours.factories import UserFactory, EstablishmentFactory, BeverageFactory
from ..models import Establishment


@pytest.mark.django_db
class TestEstablishmentAPI:
    client = APIClient()

    def test_create_establishment_api(self):
        user = UserFactory(role="partner")
        self.client.force_authenticate(user=user)
        url = reverse("v1:establishments")
        data = {
            "name": "New Establishment",
            "description": "A new sample establishment",
            "location": {"type": "Point", "coordinates": [10, 20]},
            "owner": user.id,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Establishment.objects.count() == 1
        assert Establishment.objects.get().name == "New Establishment"

    def test_retrieve_establishment_api(self):
        establishment = EstablishmentFactory()
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse("v1:establishment-detail", kwargs={"pk": establishment.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_establishment_api(self):
        user = UserFactory()
        establishment = EstablishmentFactory(owner=user)
        self.client.force_authenticate(user=user)
        url = reverse("v1:establishment-detail", kwargs={"pk": establishment.pk})
        new_name = "Updated Name"
        response = self.client.patch(url, {"name": new_name}, format="json")
        assert response.status_code == status.HTTP_200_OK
        establishment.refresh_from_db()
        assert establishment.name == new_name

    def test_delete_establishment_api(self):
        user = UserFactory(role="admin")
        self.client.force_authenticate(user=user)
        establishment = EstablishmentFactory()
        url = reverse("v1:establishment-detail", kwargs={"pk": establishment.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Establishment.objects.count() == 0

    def test_partner_update_unowned_establishment_api(self):
        owner_user = UserFactory(role="partner")
        other_user = UserFactory(role="partner")
        establishment = EstablishmentFactory(owner=owner_user)
        self.client.force_authenticate(user=other_user)
        url = reverse("v1:establishment-detail", kwargs={"pk": establishment.pk})
        new_description = "Unauthorized Update Attempt"
        response = self.client.patch(
            url, {"description": new_description}, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_establishment_invalid_location(self):
        user = UserFactory(role="partner")
        self.client.force_authenticate(user=user)
        url = reverse("v1:establishments")
        invalid_location_data = {
            "name": "Faulty Location Establishment",
            "description": "Has an invalid location format",
            "location": "NotAPointObject",
            "owner": user.id,
        }
        response = self.client.post(url, invalid_location_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_establishment_missing_required_fields(self):
        user = UserFactory(role="partner")
        self.client.force_authenticate(user=user)
        url = reverse("v1:establishments")
        incomplete_data = {
            "location": {"type": "Point", "coordinates": [10, 20]},
            "description": None,
            "owner": user.id,
        }
        response = self.client.post(url, incomplete_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_partner_sees_only_owned_establishments(self):
        partner_user = UserFactory(role="partner")
        other_user = UserFactory(role="partner")
        EstablishmentFactory(owner=partner_user)
        EstablishmentFactory(owner=partner_user)
        EstablishmentFactory(owner=other_user)

        self.client.force_authenticate(user=partner_user)
        url = reverse("v1:establishments")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_non_partner_sees_all_establishments(self):
        non_partner_user = UserFactory(role="client")
        EstablishmentFactory.create_batch(3)

        self.client.force_authenticate(user=non_partner_user)
        url = reverse("v1:establishments")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_partner_reaches_max_establishments(self):
        max_establishments = 5
        partner_user = UserFactory(role="partner")

        for _ in range(max_establishments):
            EstablishmentFactory(owner=partner_user)

        self.client.force_authenticate(user=partner_user)
        url = reverse("v1:establishments")
        new_establishment_data = {
            "name": "Extra Establishment",
            "description": "Should fail to create this one",
            "location": {"type": "Point", "coordinates": [10, 20]},
            "owner": partner_user.id,
        }

        response = self.client.post(url, new_establishment_data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.data
        assert (
            response.data["detail"]
            == "This partner has reached their maximum number of establishments."
        )

    def test_owner_sees_all_beverages(self):
        owner = UserFactory(role="partner")
        establishment = EstablishmentFactory(owner=owner)
        BeverageFactory(establishment=establishment, availability_status=True)
        BeverageFactory(establishment=establishment, availability_status=False)

        self.client.force_authenticate(user=owner)
        url = reverse("v1:menu-list", kwargs={"pk": establishment.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_non_owner_sees_only_available_beverages(self):
        owner = UserFactory()
        other_user = UserFactory()
        establishment = EstablishmentFactory(owner=owner)
        BeverageFactory(establishment=establishment, availability_status=True)
        BeverageFactory(establishment=establishment, availability_status=False)

        self.client.force_authenticate(user=other_user)
        url = reverse("v1:menu-list", kwargs={"pk": establishment.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_no_beverages_found(self):
        user = UserFactory()
        establishment = EstablishmentFactory()

        self.client.force_authenticate(user=user)
        url = reverse("v1:menu-list", kwargs={"pk": establishment.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (
            "No beverages found for this establishment or establishment does not exist."
            in response.data["detail"]
        )
