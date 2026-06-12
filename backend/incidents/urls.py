from django.urls import path

from .ops_views import IncidentSLAView, InterventionLogView, VolunteerListCreateView
from .dispatch_views import DispatchNearestRescueView, EvacuationChecklistView
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
    path("<int:pk>/dispatch/", DispatchNearestRescueView.as_view()),
    path("evacuation-checklist/", EvacuationChecklistView.as_view()),
    path("volunteers/", VolunteerListCreateView.as_view()),
    path("<int:pk>/interventions/", InterventionLogView.as_view()),
    path("<int:pk>/sla/", IncidentSLAView.as_view()),
]
