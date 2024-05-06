from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, get_object_or_404,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin
from happyhours.permissions import (
    IsAdmin,
    IsPartnerOwner,
    IsPartnerUser,
)
from .serializers import (
    EstablishmentSerializer,
    EstablishmentCreateUpdateSerializer,
    # MenuSerializer,
)
from .models import Establishment
from ..beverage.models import Beverage
from ..beverage.serializers import BeverageSerializer


@extend_schema(tags=["Establishments"])
class EstablishmentListView(ListAPIView):
    """
    Lists establishments based on user roles. This view is accessible to all
    authenticated users. Partners see only
    establishments they own.

    ### Access Control:
    - All authenticated users can access this view, but the listings are
    filtered by ownership for partners,
      showing only their own establishments.
    - Admins have the privilege to view all establishments across the platform

    ### Implementation Details:
    - The queryset dynamically adjusts based on the authenticated user's role,
    ensuring that users receive data
      that is relevant and appropriate to their permissions.
    """

    serializer_class = EstablishmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "partner":
            return Establishment.objects.filter(owner=user)
        return Establishment.objects.all()


@extend_schema(tags=["Establishments"])
class EstablishmentCreateView(CreateAPIView):
    """
    Creates a new establishment, restricted to partner users who can
     create up to their allowed limit.

    ### Validation:
    - Ensures that the partner has not exceeded their limit of owned establishments.
    - Checks data integrity for phone numbers and locations.

    ### Permission:
    - Restricted to authenticated partner users only.

    ### Business Logic:
    - The creation will fail with a `Permission Denied` error
    if the user has reached their limit of establishments.

    """

    queryset = Establishment.objects.all()
    serializer_class = EstablishmentCreateUpdateSerializer

    permission_classes = [IsPartnerUser]

    def perform_create(self, serializer):
        user = self.request.user
        if user.max_establishments <= Establishment.objects.filter(owner=user).count():
            raise PermissionDenied(
                "This partner has reached their maximum number of establishments."
            )
        serializer.save()


@extend_schema(tags=["Establishments"])
class EstablishmentViewSet(
    ViewSetMixin, RetrieveAPIView, UpdateAPIView, DestroyAPIView
):
    """
    Manages the CRUD operations for establishments. Retrieve is open to all users,
    update and delete are
    restricted to admins and owners, ensuring operational security and owner control.
    """

    queryset = Establishment.objects.all()

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return EstablishmentCreateUpdateSerializer
        return EstablishmentSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            permissions = [IsAuthenticated]
        elif self.action in ("update", "partial_update"):
            permissions = [IsPartnerOwner]
        else:
            permissions = [IsAdmin]
        return [permission() for permission in permissions]


@extend_schema(tags=["Establishments"])
class MenuView(viewsets.ReadOnlyModelViewSet):
    """
    Provides a view of the menu for a specific establishment,
    accessible to all authenticated users.
    """
    serializer_class = BeverageSerializer

    def get_queryset(self):
        establishment_id = self.kwargs.get("pk")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        return Beverage.objects.filter(establishment=establishment).select_related("category", "establishment")

    def list(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise NotFound(
                "No beverages found for this establishment or establishment does not exist."
            )
        return super().list(request, *args, **kwargs)
