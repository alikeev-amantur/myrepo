from django.utils import timezone
from django_filters import rest_framework as filters

from apps.beverage.models import Beverage

from django_filters import rest_framework as filters


class BeverageFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    # category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    # establishment = filters.CharFilter(field_name='establishment__name', lookup_expr='icontains')
    availability_status = filters.BooleanFilter(field_name='availability_status')
    in_happy_hour = filters.BooleanFilter(method='filter_happy_hour')

    class Meta:
        model = Beverage
        fields = ['availability_status']

    def filter_happy_hour(self, queryset, name, value):
        """
        Filter the queryset to include only beverages whose establishments are currently
        within their happy hour period.
        """
        if value:
            current_time = timezone.localtime().time()
            queryset = queryset.filter(
                establishment__happyhours_start__lte=current_time,
                establishment__happyhours_end__gte=current_time
            )
        return queryset