from rest_framework import generics, permissions

from .models import CropListing
from .listings_serializers import CropListingSerializer


class ListingListCreateView(generics.ListCreateAPIView):
    serializer_class = CropListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["crop_type", "region", "status"]

    def get_queryset(self):
        return CropListing.objects.filter(status=CropListing.Status.ACTIVE)


class MyListingsView(generics.ListAPIView):
    serializer_class = CropListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CropListing.objects.filter(seller=self.request.user)
