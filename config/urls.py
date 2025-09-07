"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic import RedirectView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from rest_framework.routers import DefaultRouter

from accounts.viewsets import AccountViewSet
from authentication.views import CustomTokenObtainPairView
from histories.viewsets import RainfallHistoryViewSet
from locations.viewsets import LocationViewSet
from organizations.viewsets import OrganizationViewSet
from stations.viewsets import (
    EquipmentStationViewSet,
    RainfallStationViewSet,
    StationViewSet,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="ROOC API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

router = DefaultRouter()
router.register("accounts", AccountViewSet)
router.register("locations", LocationViewSet)
router.register("histories", RainfallHistoryViewSet)
router.register("organizations", OrganizationViewSet)
router.register("stations", StationViewSet)
router.register("equipments", EquipmentStationViewSet)
router.register("rainfall", RainfallStationViewSet)


def home(request):
    return HttpResponse("pong")

class HomeView(RedirectView):
    pattern_name = "admin:index"

urlpatterns = [
    # path("", home, name="home"),
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("api/auth/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/", include(router.urls)),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
