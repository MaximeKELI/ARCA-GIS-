from django.urls import path

from .views import ShipmentListCreateView, ShipmentQuoteView, TransporterListView

urlpatterns = [
    path("transporters/", TransporterListView.as_view()),
    path("shipments/", ShipmentListCreateView.as_view()),
    path("shipments/<int:pk>/quote/", ShipmentQuoteView.as_view()),
]
