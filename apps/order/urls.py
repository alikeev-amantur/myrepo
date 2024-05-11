from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PlaceOrderView, ClientOrderHistoryView, PartnerOrderHistoryView

router = DefaultRouter()
router.register(
    r"partner-order-history", PartnerOrderHistoryView, basename="partner-order-history"
)
router.register(
    r"client-order-history", ClientOrderHistoryView, basename="client-order-history"
)
urlpatterns = [
    path("place-order/", PlaceOrderView.as_view(), name="place-order"),
    path("", include(router.urls)),
]
