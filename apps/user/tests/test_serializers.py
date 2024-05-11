import pytest

from happyhours.factories import UserFactory
from django.test import RequestFactory

from ..serializers import UserSerializer, PartnerProfileSerializer


@pytest.fixture
def client_user():
    return UserFactory(role="client")


@pytest.fixture
def partner_user():
    return UserFactory(role="partner")


@pytest.fixture
def mock_request(client_user):
    request = RequestFactory().get("/fake-url")
    request.user = client_user
    return request


@pytest.mark.django_db
def test_validate_client(client_user, mock_request):
    serializer = UserSerializer(context={"request": mock_request})
    assert serializer.validate(client_user) == client_user


@pytest.mark.django_db
def test_validate_partner(partner_user, mock_request):
    serializer = PartnerProfileSerializer(context={"request": mock_request})
    assert serializer.validate(partner_user) == partner_user
