from django.urls import path

from .views import SoilAtLocationView, SoilZoneListView

urlpatterns = [
    path("zones/", SoilZoneListView.as_view()),
    path("at-location/", SoilAtLocationView.as_view()),
]
