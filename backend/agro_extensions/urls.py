from django.urls import path

from .views import (
    AgroforestryListCreateView, BeeHiveListCreateView, CompostListCreateView,
    CropRotationPlanView, FishPondListCreateView, SeedBankListCreateView,
)

urlpatterns = [
    path("beekeeping/hives/", BeeHiveListCreateView.as_view()),
    path("aquaculture/ponds/", FishPondListCreateView.as_view()),
    path("agroforestry/plots/", AgroforestryListCreateView.as_view()),
    path("seedbank/", SeedBankListCreateView.as_view()),
    path("compost/", CompostListCreateView.as_view()),
    path("rotation-plan/", CropRotationPlanView.as_view()),
]
