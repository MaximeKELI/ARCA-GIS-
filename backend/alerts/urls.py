from django.urls import path

from .views import AlertDetailView, AlertListView, BroadcastAlertView, MarkAlertReadView

urlpatterns = [
    path("", AlertListView.as_view(), name="alert-list"),
    path("broadcast/", BroadcastAlertView.as_view(), name="alert-broadcast"),
    path("<int:pk>/", AlertDetailView.as_view(), name="alert-detail"),
    path("<int:pk>/read/", MarkAlertReadView.as_view(), name="alert-read"),
]
