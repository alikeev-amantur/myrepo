import django_filters

from .models import Establishment


class EstablishmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    location_char = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Establishment
        fields = (
            "name",
            "location_char",
        )
