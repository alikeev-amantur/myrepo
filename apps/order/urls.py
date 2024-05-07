from django.urls import path
from .views import PlaceOrderView, ClientOrderHistoryView, PartnerOrderHistoryView

urlpatterns = [
    path("place-order/", PlaceOrderView.as_view(), name="place-order"),
    path(
        "client-orders/", ClientOrderHistoryView.as_view(), name="client-order-history"
    ),
    path(
        "partner-orders/",
        PartnerOrderHistoryView.as_view(),
        name="partner-order-history",
    ),
]
