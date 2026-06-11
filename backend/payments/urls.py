from django.urls import path

from .views import PaymentHistoryView, PaymentInitiateView, PaymentVerifyView

urlpatterns = [
    path("initiate/", PaymentInitiateView.as_view()),
    path("verify/<str:reference>/", PaymentVerifyView.as_view()),
    path("history/", PaymentHistoryView.as_view()),
]
