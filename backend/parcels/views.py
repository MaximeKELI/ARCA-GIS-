from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import generics, permissions

from users.permissions import IsAdmin, IsFarmer

from .models import Parcel
from .serializers import ParcelListSerializer, ParcelSerializer


class ParcelListCreateView(generics.ListCreateAPIView):
    filterset_fields = ["crop_type", "health_status", "is_active"]
    search_fields = ["name", "notes"]

    def get_serializer_class(self):
        if self.request.method == "GET" and self.request.query_params.get("format") != "geojson":
            return ParcelListSerializer
        return ParcelSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return Parcel.objects.all()
        return Parcel.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsFarmer()]
        return [permissions.IsAuthenticated()]


class ParcelDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParcelSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return Parcel.objects.all()
        return Parcel.objects.filter(owner=user)


class NearbyParcelsView(generics.ListAPIView):
    serializer_class = ParcelListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")
        radius_km = float(self.request.query_params.get("radius", 50))

        if not lat or not lng:
            return Parcel.objects.none()

        point = Point(float(lng), float(lat), srid=4326)
        return Parcel.objects.filter(
            geometry__distance_lte=(point, D(km=radius_km)),
            is_active=True,
        )
