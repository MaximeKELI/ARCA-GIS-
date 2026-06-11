from django.urls import path

from .views import DroneMissionDetailView, DroneMissionListCreateView

urlpatterns = [
    path("missions/", DroneMissionListCreateView.as_view()),
    path("missions/<int:pk>/", DroneMissionDetailView.as_view()),
]
