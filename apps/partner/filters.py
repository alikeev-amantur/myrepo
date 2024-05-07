from django.utils import timezone
from django_filters import rest_framework as filters
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from .models import Establishment
from ..beverage.models import Beverage


class EstablishmentFilter(filters.FilterSet):
    near_me = filters.NumberFilter(method="filter_distance")
    happyhours_active = filters.BooleanFilter(method="filter_happyhours_active")

    class Meta:
        model = Establishment
        fields = []

    def filter_distance(self, queryset, name, value):
        latitude = self.request.query_params.get("latitude", None)
        longitude = self.request.query_params.get("longitude", None)
        if latitude and longitude and value:
            latitude = float(latitude)
            longitude = float(longitude)
            near_me = float(value)
            reference_location = Point(longitude, latitude, srid=4326)
            queryset = queryset.annotate(
                distance=Distance("location", reference_location)
            ).filter(distance__lte=near_me)
        return queryset

    def filter_happyhours_active(self, queryset, name, value):
        now = timezone.localtime().time()
        if value:
            return queryset.filter(happyhours_start__lte=now, happyhours_end__gte=now)
        return queryset


class MenuFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Beverage
        fields = ["category"]
