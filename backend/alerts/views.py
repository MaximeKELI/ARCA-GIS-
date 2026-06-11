from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdmin

from .models import Alert
from .serializers import AlertSerializer
from .services import broadcast_alert


class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    filterset_fields = ["alert_type", "severity", "is_read"]

    def get_queryset(self):
        user = self.request.user
        qs = Alert.objects.filter(is_broadcast=True)
        if not user.is_admin_user:
            qs = qs.filter(target_user__isnull=True) | qs.filter(target_user=user)
        return qs


class AlertDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AlertSerializer

    def get_queryset(self):
        return Alert.objects.all()

    def perform_update(self, serializer):
        serializer.save()


class MarkAlertReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response({"error": "Alerte introuvable"}, status=status.HTTP_404_NOT_FOUND)
        alert.is_read = True
        alert.save(update_fields=["is_read"])
        return Response(AlertSerializer(alert).data)


class BroadcastAlertView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        alert = broadcast_alert(
            alert_type=request.data.get("alert_type", "system"),
            title=request.data.get("title", "Alerte système"),
            message=request.data.get("message", ""),
            severity=request.data.get("severity", "medium"),
            data=request.data.get("data", {}),
            target_role=request.data.get("target_role", ""),
        )
        return Response(AlertSerializer(alert).data, status=status.HTTP_201_CREATED)
