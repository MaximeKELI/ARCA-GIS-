from django.urls import path

from .views import NearbyParcelsView, ParcelDetailView, ParcelListCreateView

urlpatterns = [
    path("", ParcelListCreateView.as_view(), name="parcel-list"),
    path("nearby/", NearbyParcelsView.as_view(), name="parcel-nearby"),
    path("<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail"),
]
