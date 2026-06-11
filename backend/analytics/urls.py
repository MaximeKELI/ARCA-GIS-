from django.urls import path

from .ngo_views import NGOExportView, NGOStatsView
from .views import (
    AnalyticsSnapshotListView,
    CropHistoryListView,
    DashboardStatsView,
    RecordCropHistoryView,
)

urlpatterns = [
    path("dashboard/", DashboardStatsView.as_view()),
    path("crop-history/", CropHistoryListView.as_view()),
    path("crop-history/record/", RecordCropHistoryView.as_view()),
    path("snapshots/", AnalyticsSnapshotListView.as_view()),
]
