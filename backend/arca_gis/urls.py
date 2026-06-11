from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", TemplateView.as_view(template_name="dashboard/index.html"), name="dashboard"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", include("users.urls")),
    path("api/parcels/", include("parcels.urls")),
    path("api/climate/", include("climate.urls")),
    path("api/incidents/", include("incidents.urls")),
    path("api/alerts/", include("alerts.urls")),
    path("api/core/", include("core.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/iot/", include("iot.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/cooperatives/", include("cooperatives.urls")),
    path("api/marketplace/", include("marketplace.urls")),
    path("api/drones/", include("drones.urls")),
    path("api/traceability/", include("traceability.urls")),
    path("api/communications/", include("communications.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/soils/", include("soils.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
