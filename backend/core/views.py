from django.contrib.gis.geos import Point
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.services import broadcast_alert
from climate.services import request_ai_analysis
from parcels.models import Parcel
from users.permissions import IsAdmin

from .models import AuditLog, GeofenceZone, OfflineSyncQueue
from .serializers import AuditLogSerializer, GeofenceZoneSerializer, OfflineSyncSerializer
from .services import check_geofence, generate_parcel_report


class GeofenceListCreateView(generics.ListCreateAPIView):
    queryset = GeofenceZone.objects.filter(is_active=True)
    serializer_class = GeofenceZoneSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class GeofenceCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        if not lat or not lng:
            return Response({"error": "lat/lng requis"}, status=400)

        zones = check_geofence(float(lat), float(lng), request.user)
        for zone in zones:
            if zone["alert_on_enter"]:
                broadcast_alert(
                    alert_type="system",
                    title=f"⚠️ Zone: {zone['name']}",
                    message=zone.get("description", f"Entrée dans {zone['name']}"),
                    severity="high" if zone["zone_type"] == "risk" else "medium",
                    data=zone,
                    target_user=request.user,
                )
        return Response({"zones": zones, "count": len(zones)})


class ParcelReportPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            parcel = Parcel.objects.get(pk=pk)
        except Parcel.DoesNotExist:
            return Response({"error": "Parcelle introuvable"}, status=404)

        if not request.user.is_admin_user and parcel.owner != request.user:
            return Response({"error": "Accès refusé"}, status=403)

        analysis = None
        if parcel.geometry:
            c = parcel.geometry.centroid
            analysis = request_ai_analysis(c.y, c.x, parcel.crop_type)

        pdf = generate_parcel_report(parcel, analysis)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="rapport_{parcel.name}.pdf"'
        return response


class OfflineSyncView(generics.ListCreateAPIView):
    serializer_class = OfflineSyncSerializer

    def get_queryset(self):
        return OfflineSyncQueue.objects.filter(user=self.request.user, synced=False)

    def perform_create(self, serializer):
        from .sync_handlers import process_offline_item
        item = serializer.save()
        if process_offline_item(item):
            item.synced = True
            item.save()


class OfflineSyncProcessView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        items = OfflineSyncQueue.objects.filter(user=request.user, synced=False)
        count = 0
        from .sync_handlers import process_offline_item
        for item in items:
            if process_offline_item(item):
                count += 1
                item.synced = True
                item.save()
        return Response({"synced": count})


class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    queryset = AuditLog.objects.all()[:200]
