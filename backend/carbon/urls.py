from django.urls import path

from .views import CarbonCreditListView, CarbonEstimateView

urlpatterns = [
    path("credits/", CarbonCreditListView.as_view()),
    path("estimate/", CarbonEstimateView.as_view()),
]
