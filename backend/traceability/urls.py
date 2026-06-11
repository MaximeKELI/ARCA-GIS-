from django.urls import path

from .views import HarvestListCreateView, VerifyCertificateView

urlpatterns = [
    path("harvests/", HarvestListCreateView.as_view()),
    path("verify/<str:cert_id>/", VerifyCertificateView.as_view()),
]
