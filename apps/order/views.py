from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.beverage.models import Beverage
from apps.order.models import Order
from apps.order.serializers import OrderSerializer, OrderHistorySerializer
from apps.partner.models import Establishment


@extend_schema(tags=["Orders"], responses={201: OrderSerializer, 400: OrderSerializer})
class PlaceOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        beverage_id = serializer.validated_data.get("beverage").id
        beverage = Beverage.objects.get(id=beverage_id)
        serializer.save(client=self.request.user, establishment=beverage.establishment)


@extend_schema(tags=["Orders"])
class ClientOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


@extend_schema(tags=["Orders"])
class PartnerOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owned_establishments = Establishment.objects.filter(owner=self.request.user)
        return Order.objects.filter(establishment__in=owned_establishments)
