from django.urls import path

from .views import AwardPointsView, LeaderboardView, MyGamificationView

urlpatterns = [
    path("me/", MyGamificationView.as_view()),
    path("award/", AwardPointsView.as_view()),
    path("leaderboard/", LeaderboardView.as_view()),
]
