from django.urls import path

from .v7_views import CastVoteView, EquipmentReserveView, VoteListCreateView
from .views import CooperativeDetailView, CooperativeListCreateView, JoinCooperativeView

urlpatterns = [
    path("", CooperativeListCreateView.as_view()),
    path("<int:pk>/", CooperativeDetailView.as_view()),
    path("<int:pk>/join/", JoinCooperativeView.as_view()),
    path("votes/", VoteListCreateView.as_view()),
    path("votes/<int:pk>/cast/", CastVoteView.as_view()),
    path("equipment/", EquipmentReserveView.as_view()),
]
