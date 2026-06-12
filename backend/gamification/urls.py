from django.urls import path

from .challenge_views import ChallengeListView, RegionalLeaderboardView
from .views import AwardPointsView, LeaderboardView, MyGamificationView

urlpatterns = [
    path("me/", MyGamificationView.as_view()),
    path("award/", AwardPointsView.as_view()),
    path("leaderboard/", LeaderboardView.as_view()),
    path("leaderboard/regional/", RegionalLeaderboardView.as_view()),
    path("challenges/", ChallengeListView.as_view()),
]
