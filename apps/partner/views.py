from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404, ListCreateAPIView,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin
from happyhours.permissions import (
    IsAdmin,
    IsPartnerOwner,
    IsPartnerUser,
)
from .filters import EstablishmentFilter, MenuFilter
from .serializers import (
    EstablishmentSerializer,
    EstablishmentCreateUpdateSerializer,
    # MenuSerializer,
)
from .models import Establishment
from ..beverage.models import Beverage
from ..beverage.serializers import BeverageSerializer


@extend_schema(tags=["Establishments"])
class EstablishmentListCreateView(ListCreateAPIView):
    """
    Get a list of establishments or create a new establishment.
    - List is accessible to all authenticated users. Partners see only the establishments they own.
    - Creation is restricted to partner users who can create up to their allowed limit.

    ### Implementation Details:
    - The queryset dynamically adjusts based on the authenticated user's role,
    ensuring that users receive data that is relevant and appropriate to their permissions.
    - Ensures that the partner has not exceeded their limit of owned establishments.
    - Checks data integrity for phone numbers and locations during creation.
    """

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EstablishmentCreateUpdateSerializer
        return EstablishmentSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = EstablishmentFilter
    search_fields = ["name", "beverages__name"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "partner":
            return Establishment.objects.filter(owner=user)
        return Establishment.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsPartnerUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.max_establishments <= Establishment.objects.filter(owner=user).count():
            raise PermissionDenied(
                "This partner has reached their maximum number of establishments."
            )
        serializer.save(owner=user)


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        establishment_id = self.kwargs.get("pk")
        establishment = get_object_or_404(Establishment, id=establishment_id)
        user = self.request.user

        if user == establishment.owner:
            return Beverage.objects.filter(establishment=establishment).select_related(
                "category", "establishment"
            )

        return Beverage.objects.filter(
            establishment=establishment, availability_status=True
        ).select_related("category", "establishment")

    def list(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise NotFound(
                "No beverages found for this establishment or establishment does not exist."
            )
        return super().list(request, *args, **kwargs)
