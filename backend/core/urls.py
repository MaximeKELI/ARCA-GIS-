from django.urls import path

from .gdpr_views import ConsentView, DataDeleteView, DataExportView
from .views import (
    AuditLogListView,
    GeofenceCheckView,
    GeofenceListCreateView,
    OfflineSyncProcessView,
    OfflineSyncView,
    ParcelReportPDFView,
)

urlpatterns = [
    path("geofences/", GeofenceListCreateView.as_view()),
    path("geofences/check/", GeofenceCheckView.as_view()),
    path("reports/parcel/<int:pk>/", ParcelReportPDFView.as_view()),
    path("offline/sync/", OfflineSyncView.as_view()),
    path("offline/process/", OfflineSyncProcessView.as_view()),
    path("audit/", AuditLogListView.as_view()),
]
