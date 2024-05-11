from django.urls import path

from .views import (
    EstablishmentListCreateView,
    EstablishmentViewSet,
    MenuView,
)

urlpatterns = [
    path(
        "establishments/",
        EstablishmentListCreateView.as_view(),
        name="establishments",
    ),
    path(
        "establishments/<int:pk>/",
        EstablishmentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="establishment-detail",
    ),
    path("menu/<int:pk>/", MenuView.as_view({"get": "list"}), name="menu-list"),
]
