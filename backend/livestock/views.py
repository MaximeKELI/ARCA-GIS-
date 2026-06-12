from rest_framework import generics, permissions

from .models import Herd, VeterinaryAlert
from .serializers import HerdSerializer, VeterinaryAlertSerializer


class HerdListCreateView(generics.ListCreateAPIView):
    serializer_class = HerdSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["animal_type", "health_status"]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return Herd.objects.all()
        return Herd.objects.filter(owner=user)


class HerdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HerdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return Herd.objects.all()
        return Herd.objects.filter(owner=user)


class VeterinaryAlertListView(generics.ListAPIView):
    serializer_class = VeterinaryAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = VeterinaryAlert.objects.filter(is_active=True)
