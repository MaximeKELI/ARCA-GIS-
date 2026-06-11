from django.urls import path

from .views import ClaimListView, EvaluateClaimView, PolicyListCreateView

urlpatterns = [
    path("policies/", PolicyListCreateView.as_view()),
    path("claims/", ClaimListView.as_view()),
    path("policies/<int:pk>/evaluate/", EvaluateClaimView.as_view()),
]
