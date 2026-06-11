from django.urls import path

from .views import ProfileView, RegisterView, RescueTeamView, UserDetailView, UserListView
from .views_2fa import Enable2FAView, Setup2FAView, Verify2FAView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("2fa/setup/", Setup2FAView.as_view()),
    path("2fa/enable/", Enable2FAView.as_view()),
    path("2fa/verify/", Verify2FAView.as_view()),
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("rescue-team/", RescueTeamView.as_view(), name="rescue-team"),
]
