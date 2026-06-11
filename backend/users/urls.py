from django.urls import path

from .views import ProfileView, RegisterView, RescueTeamView, UserDetailView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("rescue-team/", RescueTeamView.as_view(), name="rescue-team"),
]
