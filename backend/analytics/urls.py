from django.urls import path

from .role_dashboards import AdminDashboardView, FarmerDashboardView, RescueDashboardView, RoleDashboardRouterView
from .heatmap_views import YieldHeatmapView
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
    path("ngo/stats/", NGOStatsView.as_view()),
    path("ngo/export/", NGOExportView.as_view()),
    path("heatmap/", YieldHeatmapView.as_view()),
]
