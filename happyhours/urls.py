"""
URL configuration for happyhours project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include, re_path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)

v1_api = (
    [
        path('beverage/', include('apps.beverage.urls')),
        path('order/', include('apps.order.urls')),
        path('partner/', include('apps.partner.urls')),
        path('user/', include('apps.user.urls')),
        path('feedback/', include('apps.feedback.urls')),
    ], 'v1',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'
    ),
    path(
        "api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    re_path(r'api/v1/', include(v1_api, namespace='v1'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

