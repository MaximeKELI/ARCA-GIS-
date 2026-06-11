from django.urls import path

from .views import (
    AlertDetailView, AlertListView, ApproveAlertView,
    BroadcastAlertView, MarkAlertReadView, PendingApprovalListView,
)

urlpatterns = [
    path("", AlertListView.as_view(), name="alert-list"),
    path("pending/", PendingApprovalListView.as_view()),
    path("broadcast/", BroadcastAlertView.as_view(), name="alert-broadcast"),
    path("<int:pk>/", AlertDetailView.as_view(), name="alert-detail"),
    path("<int:pk>/read/", MarkAlertReadView.as_view(), name="alert-read"),
    path("<int:pk>/approve/", ApproveAlertView.as_view()),
]
