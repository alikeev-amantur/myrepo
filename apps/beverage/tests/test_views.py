import pytest
import pytz
from django.db.models.functions import datetime
from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient
from happyhours.factories import (
    UserFactory,
    BeverageFactory,
    EstablishmentFactory,
    CategoryFactory,
)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def partner_user():
    return UserFactory(role="partner")


@pytest.fixture
def normal_user():
    return UserFactory(role="client")


@pytest.fixture
def partner_establishment(partner_user):
    return EstablishmentFactory(owner=partner_user)


@pytest.fixture
def beverage(partner_establishment):
    return BeverageFactory(establishment=partner_establishment)


@pytest.fixture
def establishment_happy_hour():
    return EstablishmentFactory(happyhours_start="15:00:00", happyhours_end="17:00:00")


@pytest.fixture
def establishment_not_happy_hour():
    return EstablishmentFactory(happyhours_start="18:00:00", happyhours_end="20:00:00")


@pytest.fixture
def beverage_in_happy_hour(establishment_happy_hour):
    return BeverageFactory(establishment=establishment_happy_hour)


@pytest.fixture
def beverage_not_in_happy_hour(establishment_not_happy_hour):
    return BeverageFactory(establishment=establishment_not_happy_hour)


@pytest.mark.django_db
def test_retrieve_beverage_authenticated(client, normal_user, beverage):
    client.force_authenticate(user=normal_user)
    url = reverse("v1:beverage-detail", args=[beverage.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_beverage_permission_denied(client, normal_user):
    client.force_authenticate(user=normal_user)
    url = reverse("v1:beverage-list")
    data = {"name": "Test Beverage", "price": 10.99}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_beverage_as_partner(client, partner_user, partner_establishment):
    client.force_authenticate(user=partner_user)
    url = reverse("v1:beverage-list")
    data = {
        "name": "New Beverage",
        "price": 10.99,
        "description": "Some description",
        "establishment": partner_establishment.id,
        "category": CategoryFactory().id,
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_search_beverage_by_name(client, normal_user, beverage):
    client.force_authenticate(user=normal_user)
    url = reverse("v1:beverage-list") + f"?search={beverage.name}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["name"] == beverage.name


@pytest.mark.django_db
def test_filter_beverage_by_category(client, normal_user, beverage):
    client.force_authenticate(user=normal_user)
    url = reverse("v1:beverage-list") + f"?category={beverage.category.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["name"] == beverage.name


@pytest.mark.django_db
@freeze_time(
    pytz.timezone("Asia/Bishkek")
    .localize(datetime.datetime(2023, 5, 1, 16, 0))
    .astimezone(pytz.utc)
)
def test_filter_beverage_in_happy_hour(
    client, normal_user, beverage_in_happy_hour, beverage_not_in_happy_hour
):
    client.force_authenticate(user=normal_user)
    url = reverse("v1:beverage-list") + "?in_happy_hour=true"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    print("Filtered data:", response.data)  # Debugging output
    assert len(response.data) == 1, "Should find exactly one beverage in happy hour"
    assert (
        response.data[0]["id"] == beverage_in_happy_hour.id
    ), "The beverage should be the one in happy hour"


@pytest.mark.django_db
@freeze_time(
    pytz.timezone("Asia/Bishkek")
    .localize(datetime.datetime(2023, 5, 1, 23, 0))
    .astimezone(pytz.utc)
)
def test_filter_beverage_not_in_happy_hour(
    client, normal_user, beverage_in_happy_hour, beverage_not_in_happy_hour
):
    client.force_authenticate(user=normal_user)
    url = reverse("v1:beverage-list") + "?in_happy_hour=true"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0, "Should find no beverages in happy hour"
