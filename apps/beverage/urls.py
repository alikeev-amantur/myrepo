from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BeverageViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"beverages", BeverageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
