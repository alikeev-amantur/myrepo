import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from happyhours.factories import BeverageFactory, EstablishmentFactory, CategoryFactory, UserFactory
from ..serializers import BeverageSerializer
from django.test import RequestFactory
User = get_user_model()

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def another_user():
    return UserFactory()
@pytest.fixture
def mock_request(user):
    request = RequestFactory().get('/fake-url')
    request.user = user
    return request

@pytest.fixture
def category():
    return CategoryFactory()

@pytest.fixture
def establishment(user):
    return EstablishmentFactory(owner=user)

@pytest.fixture
def beverage(establishment, category):
    return BeverageFactory(establishment=establishment, category=category)

@pytest.mark.django_db
def test_validate_establishment_with_owner(establishment, mock_request):
    serializer = BeverageSerializer(context={'request': mock_request})
    assert serializer.validate_establishment(establishment) == establishment

@pytest.mark.django_db
def test_validate_establishment_not_owner(establishment, another_user, mock_request):
    mock_request.user = another_user
    serializer = BeverageSerializer(context={'request': mock_request})
    with pytest.raises(ValidationError) as excinfo:
        serializer.validate_establishment(establishment)
    assert "User does not own this establishment." in str(excinfo.value)

@pytest.mark.django_db
def test_validate_price_positive():
    serializer = BeverageSerializer()
    assert serializer.validate_price(10) == 10

@pytest.mark.django_db
def test_validate_price_negative():
    serializer = BeverageSerializer()
    with pytest.raises(ValidationError) as excinfo:
        serializer.validate_price(-1)
    assert "The price must be a non-negative number." in str(excinfo.value)

@pytest.mark.django_db
def test_to_representation(beverage):
    serializer = BeverageSerializer(beverage)
    result = serializer.to_representation(beverage)
    assert result['category'] == beverage.category.name
    assert result['establishment'] == beverage.establishment.name

