import pytest
from unittest.mock import patch, Mock
from django.utils import timezone
import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from happyhours.factories import UserFactory, BeverageFactory, EstablishmentFactory
from ..serializers import OrderSerializer


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def establishment():
    return EstablishmentFactory()


@pytest.fixture
def beverage(establishment):
    return BeverageFactory(establishment=establishment)

@pytest.mark.django_db
def test_order_serializer_fields(user, beverage):
    order_data = {
        'beverage': beverage.id,
        'client': user.id,
        'establishment': beverage.establishment.id,
        'order_date': timezone.now()
    }
    serializer = OrderSerializer(data=order_data)
    assert serializer.fields['client'].read_only
    assert serializer.fields['establishment'].read_only
    assert 'id' in serializer.fields
    assert 'beverage' in serializer.fields

@pytest.mark.django_db
def test_get_default_establishment(beverage):
    serializer = OrderSerializer()
    establishment = serializer.get_default_establishment(beverage)
    assert establishment == beverage.establishment

@pytest.mark.django_db
@patch('django.utils.timezone.localtime',
       return_value=timezone.make_aware(datetime.datetime.combine(datetime.date.today(), datetime.time(11, 0))))
def test_validate_order_happyhours_inside(mock_time, establishment, user, beverage):
    establishment.happyhours_start = datetime.time(10, 0)
    establishment.happyhours_end = datetime.time(12, 0)
    serializer = OrderSerializer()
    # No exception means validation passed
    serializer.validate_order_happyhours(establishment)

@pytest.mark.django_db
@patch('django.utils.timezone.localtime',
       return_value=timezone.make_aware(datetime.datetime.combine(datetime.date.today(), datetime.time(13, 0))))
def test_validate_order_happyhours_outside(mock_time, establishment, user, beverage):
    establishment.happyhours_start = datetime.time(10, 0)
    establishment.happyhours_end = datetime.time(12, 0)
    serializer = OrderSerializer()
    with pytest.raises(ValidationError):
        serializer.validate_order_happyhours(establishment)

@pytest.mark.django_db
@patch('django.utils.timezone.localtime')
@patch('apps.order.models.Order.objects.filter')
def test_validate_order_per_hour(mock_filter, mock_time, user, beverage):
    mock_time.return_value = timezone.now()
    mock_filter.return_value.exists.return_value = True
    serializer = OrderSerializer()
    with pytest.raises(ValidationError):
        serializer.validate_order_per_hour(user)

@pytest.mark.django_db
@patch('django.utils.timezone.localtime')
@patch('apps.order.models.Order.objects.filter')
def test_validate_order_per_day(mock_filter, mock_time, user, establishment):
    mock_time.return_value = timezone.now()
    mock_filter.return_value.exists.return_value = True
    serializer = OrderSerializer()
    with pytest.raises(ValidationError):
        serializer.validate_order_per_day(user, establishment)

@pytest.mark.django_db
def test_serializer_validate_integration(user, beverage):
    with patch.object(OrderSerializer, 'validate_order_happyhours') as mock_happyhours, \
            patch.object(OrderSerializer, 'validate_order_per_hour') as mock_per_hour, \
            patch.object(OrderSerializer, 'validate_order_per_day') as mock_per_day:
        serializer = OrderSerializer(context={'request': Mock(user=user)})
        data = {'beverage': beverage}
        validated_data = serializer.validate(data)
        assert 'client' in validated_data
        assert 'establishment' in validated_data
        mock_happyhours.assert_called_once()
        mock_per_hour.assert_called_once()
        mock_per_day.assert_called_once()
