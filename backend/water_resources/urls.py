from django.urls import path

from .views import WaterConflictView, WaterPointListView, WaterQuotaListView

urlpatterns = [
    path("points/", WaterPointListView.as_view()),
    path("quotas/", WaterQuotaListView.as_view()),
    path("conflicts/", WaterConflictView.as_view()),
]
