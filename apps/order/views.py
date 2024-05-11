from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.beverage.models import Beverage
from apps.order.models import Order
from apps.order.serializers import OrderSerializer, OrderHistorySerializer
from apps.order.utils import send_order_notification
from apps.partner.models import Establishment
from happyhours.permissions import IsPartnerUser


@extend_schema(tags=["Orders"], responses={201: OrderSerializer, 400: OrderSerializer})
class PlaceOrderView(generics.CreateAPIView):
    """
    API endpoint for placing orders. Only authenticated users can create orders.

    The endpoint expects beverage ID as part of the request, and automatically sets the order's client
    to the current user and the establishment to the one associated with the specified beverage.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        beverage_id = serializer.validated_data.get("beverage").id
        beverage = Beverage.objects.get(id=beverage_id)
        order = serializer.save(client=self.request.user, establishment=beverage.establishment)
        send_order_notification(order)


@extend_schema(tags=["Orders"])
class ClientOrderHistoryView(ReadOnlyModelViewSet):
    """
    ViewSet for viewing a client's own order history.
    Provides endpoints for listing all orders associated
    with the authenticated client and for retrieving details of a specific order.
    """

    serializer_class = OrderHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


@extend_schema(tags=["Orders"])
class PartnerOrderHistoryView(ReadOnlyModelViewSet):
    """
    ViewSet for viewing order history for partners.
    Lists all orders related to establishments owned by the authenticated partner and
    allows retrieving specific orders.

    This viewset supports listing all such orders and retrieving details for a specific order.
    """

    serializer_class = OrderHistorySerializer
    permission_classes = [IsPartnerUser]

    def get_queryset(self):
        """
        This queryset returns orders for the establishments owned by the logged-in user.
        """
        owned_establishments = Establishment.objects.filter(owner=self.request.user)
        return Order.objects.filter(establishment__in=owned_establishments)
