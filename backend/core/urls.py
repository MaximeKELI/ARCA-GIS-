from django.urls import path

from .backup_views import BackupTriggerView
from .activity_views import ActivityFeedView
from .bookmark_views import BookmarkDeleteView, BookmarkListCreateView
from .oauth_views import OAuthCallbackView, OAuthProvidersView
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
    path("activity/", ActivityFeedView.as_view()),
    path("bookmarks/", BookmarkListCreateView.as_view()),
    path("bookmarks/<int:pk>/", BookmarkDeleteView.as_view()),
    path("audit/", AuditLogListView.as_view()),
    path("gdpr/consent/", ConsentView.as_view()),
    path("gdpr/export/", DataExportView.as_view()),
    path("gdpr/delete/", DataDeleteView.as_view()),
    path("backup/", BackupTriggerView.as_view()),
    path("oauth/providers/", OAuthProvidersView.as_view()),
    path("oauth/callback/", OAuthCallbackView.as_view()),
]
