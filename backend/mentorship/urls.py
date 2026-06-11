from django.urls import path

from .views import MentorshipListCreateView, SessionListCreateView

urlpatterns = [
    path("", MentorshipListCreateView.as_view()),
    path("<int:mentorship_id>/sessions/", SessionListCreateView.as_view()),
]
