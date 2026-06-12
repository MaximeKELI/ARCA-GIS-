from django.urls import path

from .views import (
    NutritionListCreateView, PictogramMenuView, VillageGroupListView,
    VoiceTranslateView, WomenProgramListCreateView,
)

urlpatterns = [
    path("village-groups/", VillageGroupListView.as_view()),
    path("women-farmers/", WomenProgramListCreateView.as_view()),
    path("nutrition/", NutritionListCreateView.as_view()),
    path("voice-translate/", VoiceTranslateView.as_view()),
    path("pictogram-menu/", PictogramMenuView.as_view()),
]
