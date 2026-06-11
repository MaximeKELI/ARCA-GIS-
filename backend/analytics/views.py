from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from climate.models import ClimateEvent
from incidents.models import Incident
from parcels.models import Parcel
from users.permissions import IsAdmin

from .models import AnalyticsSnapshot, CropHistory
from .serializers import AnalyticsSnapshotSerializer, CropHistorySerializer


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "parcels": {
                "total": Parcel.objects.filter(is_active=True).count(),
                "by_health": dict(
                    Parcel.objects.filter(is_active=True)
                    .values("health_status").annotate(c=Count("id")).values_list("health_status", "c")
                ),
                "avg_moisture": Parcel.objects.filter(is_active=True).aggregate(
                    avg=Avg("soil_moisture")
                )["avg"],
            },
            "incidents": {
                "total": Incident.objects.count(),
                "active_sos": Incident.objects.filter(
                    is_sos=True, status__in=["pending", "acknowledged", "in_progress"]
                ).count(),
                "resolved": Incident.objects.filter(status="resolved").count(),
            },
            "climate": {
                "active_events": ClimateEvent.objects.filter(is_active=True).count(),
                "by_type": dict(
                    ClimateEvent.objects.filter(is_active=True)
                    .values("event_type").annotate(c=Count("id")).values_list("event_type", "c")
                ),
            },
            "alerts": {
                "unread": Alert.objects.filter(is_read=False).count(),
                "total": Alert.objects.count(),
            },
        })


class CropHistoryListView(generics.ListAPIView):
    serializer_class = CropHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        parcel_id = self.request.query_params.get("parcel")
        qs = CropHistory.objects.all()
        if parcel_id:
            qs = qs.filter(parcel_id=parcel_id)
        elif not self.request.user.is_admin_user:
            qs = qs.filter(parcel__owner=self.request.user)
        return qs[:90]


class AnalyticsSnapshotListView(generics.ListAPIView):
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = [IsAdmin]
    queryset = AnalyticsSnapshot.objects.all()[:30]


class RecordCropHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        parcel_id = request.data.get("parcel_id")
        try:
            parcel = Parcel.objects.get(pk=parcel_id)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcelle introuvable"}, status=404)

        history = CropHistory.objects.create(
            parcel=parcel,
            health_status=parcel.health_status,
            soil_moisture=parcel.soil_moisture,
            temperature=request.data.get("temperature"),
            rainfall_mm=request.data.get("rainfall_mm"),
            ndvi_score=request.data.get("ndvi_score"),
            recorded_at=timezone.now(),
        )
        return Response(CropHistorySerializer(history).data, status=201)
