import datetime

import pytest
from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..utils import datetime_serializer

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:
    client = APIClient()

    def test_client_login(self, client, django_user_model):
        email = "user@example.com"
        password = "somepassword1"
        role = "client"
        user = django_user_model.objects.create_user(
            email=email, password=password, role=role
        )
        client.login(email=email, password=password)
        url = reverse("v1:token_obtain_pair")
        data = {
            "email": email,
            "password": password,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_blocked_user(self, django_user_model):
        email = "user@example.com"
        password = "somepassword1"
        role = "client"
        is_blocked = True
        user = django_user_model.objects.create_user(
            email=email, password=password, role=role, is_blocked=is_blocked
        )
        url = reverse("v1:token_obtain_pair")
        data = {
            "email": email,
            "password": password,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_forgot_page(self):
        url = reverse("v1:password-forgot-page")
        data = {
            "email": "email",
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reset_code(self):
        session = self.client.session
        session["reset_code"] = "9267"
        session["reset_code_create_time"] = datetime_serializer(datetime.datetime.now())
        session.save()
        url = reverse("v1:password-reset")
        data = {
            "email": "email@example.com",
            "reset_code": "9263",
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
