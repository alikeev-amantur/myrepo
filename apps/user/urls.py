from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)

from .views import (
    UserViewSet,
    ClientRegisterView,
    CreatePartner,
    ClientListView,
    TokenObtainView,
    ClientPasswordForgotPageView,
    ClientPasswordResetView,
    ClientPasswordChangeView,
    AdminLoginView,
    PartnerListView,
    BlockUserView,
)

TokenBlacklistView = extend_schema(tags=["Users"])(TokenBlacklistView)
TokenRefreshView = extend_schema(tags=["Users"])(TokenRefreshView)

urlpatterns = [
    path("token/", TokenObtainView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/admin/", AdminLoginView.as_view(), name="admin_login"),
    path("client_register/", ClientRegisterView.as_view(), name="client-register"),
    path("client_list/", ClientListView.as_view(), name="client-list"),
    path("partner_list", PartnerListView.as_view(), name="partner-list"),
    path("block_user/", BlockUserView.as_view(), name="block-user"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("create_partner/", CreatePartner.as_view(), name="create-partner"),
    path(
        "",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ), name="user-detail",
    ),
    path(
        'password_forgot/', ClientPasswordForgotPageView.as_view(),
        name='password-forgot-page'
    ),
    path(
        'password_reset/', ClientPasswordResetView.as_view(),
        name='password-reset'
    ),
    path(
        'password_change/', ClientPasswordChangeView.as_view(),
        name='password-change'
    ),
]
