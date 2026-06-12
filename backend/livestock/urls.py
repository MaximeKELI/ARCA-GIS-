from django.urls import path

from .views import HerdDetailView, HerdListCreateView, VeterinaryAlertListView

urlpatterns = [
    path("herds/", HerdListCreateView.as_view()),
    path("herds/<int:pk>/", HerdDetailView.as_view()),
    path("vet-alerts/", VeterinaryAlertListView.as_view()),
]
