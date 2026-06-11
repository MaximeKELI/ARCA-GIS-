from rest_framework import generics, permissions

from .models import DroneMission
from .serializers import DroneMissionSerializer


class DroneMissionListCreateView(generics.ListCreateAPIView):
    serializer_class = DroneMissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "mission_type"]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user or user.role in ("agent", "government"):
            return DroneMission.objects.all()
        return DroneMission.objects.filter(operator=user)


class DroneMissionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = DroneMissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DroneMission.objects.all()
