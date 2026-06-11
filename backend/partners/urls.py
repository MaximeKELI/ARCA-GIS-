from django.urls import path

from .views import PartnerDataView, PartnerKeyListView

urlpatterns = [
    path("keys/", PartnerKeyListView.as_view()),
    path("data/", PartnerDataView.as_view()),
]
