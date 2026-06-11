from django.urls import path

from .views import (
    ActiveSOSListView,
    AssignIncidentView,
    IncidentDetailView,
    IncidentListCreateView,
    SOSView,
)

urlpatterns = [
    path("", IncidentListCreateView.as_view(), name="incident-list"),
    path("sos/", SOSView.as_view(), name="incident-sos"),
    path("sos/active/", ActiveSOSListView.as_view(), name="incident-sos-active"),
    path("<int:pk>/", IncidentDetailView.as_view(), name="incident-detail"),
    path("<int:pk>/assign/", AssignIncidentView.as_view(), name="incident-assign"),
]
