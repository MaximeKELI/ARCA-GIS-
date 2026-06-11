from django.urls import path

from .views import ChatMessageListCreateView

urlpatterns = [
    path("<int:incident_id>/", ChatMessageListCreateView.as_view()),
]
