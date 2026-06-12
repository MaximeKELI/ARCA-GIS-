from django.urls import path

from .views import AdvisorChatView, DiseaseDetectView, VoiceJournalView, WeeklyPlannerView

urlpatterns = [
    path("chat/", AdvisorChatView.as_view()),
    path("disease/", DiseaseDetectView.as_view()),
    path("planner/", WeeklyPlannerView.as_view()),
    path("voice-journal/", VoiceJournalView.as_view()),
]
