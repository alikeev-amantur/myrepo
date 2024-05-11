import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from happyhours.factories import (
    UserFactory,
    CategoryFactory,
    BeverageFactory,
    EstablishmentFactory,
)


@pytest.mark.django_db
class TestCategoryViewSetPermissions:
    def setup_method(self):
        self.client = APIClient()
        self.admin_user = UserFactory(role="admin")
        self.regular_user = UserFactory(role="user")
        self.category = CategoryFactory()
        self.url_list = reverse("v1:category-list")
        self.url_detail = reverse("v1:category-detail", args=[self.category.id])

    def test_list_categories_permissions(self):
        assert self.category is not None
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url_list)
        assert response.status_code == status.HTTP_200_OK

        self.client.logout()
        response = self.client.get(self.url_list)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_category_permissions(self):
        data = {"name": "New Category"}

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.url_list, data)
        assert response.status_code == status.HTTP_201_CREATED

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.url_list, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_category_permissions(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.url_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.url_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestBeverageViewSetPermissions:
    def setup_method(self):
        self.client = APIClient()
        self.partner_user = UserFactory(role="partner", max_establishments=4)
        self.partner_owner_user = UserFactory(role="partner")
        self.regular_user = UserFactory(role="client")
        self.establishment = EstablishmentFactory(owner=self.partner_owner_user)
        self.beverage = BeverageFactory(establishment=self.establishment)
        self.category = CategoryFactory()
        self.list_url = reverse("v1:beverage-list")
        self.detail_url = reverse("v1:beverage-detail", args=[self.beverage.id])

    def test_list_beverages_permissions(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK

        self.client.logout()
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_beverage_permissions(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK

        self.client.logout()
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_beverage_permissions(self):
        self.client.force_authenticate(user=self.partner_user)
        establishment = EstablishmentFactory(owner=self.partner_user)
        response = self.client.post(
            self.list_url,
            {
                "name": "New Beverage",
                "price": "5.99",
                "description": "some text",
                "category": self.category.id,
                "establishment": establishment.id,
            },
        )
        print(response)
        assert response.status_code == status.HTTP_201_CREATED

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(
            self.list_url, {"name": "Another Beverage", "price": "6.99"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_beverage_permissions(self):
        self.client.force_authenticate(user=self.partner_owner_user)
        response = self.client.patch(self.detail_url, {"price": 7.99})
        assert response.status_code == status.HTTP_200_OK

        self.client.force_authenticate(user=self.partner_user)
        response = self.client.patch(self.detail_url, {"price": 8.99})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_beverage_permissions(self):
        self.client.force_authenticate(user=self.partner_owner_user)
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.beverage = BeverageFactory()
        detail_url = reverse("v1:beverage-detail", args=[self.beverage.id])
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(detail_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
