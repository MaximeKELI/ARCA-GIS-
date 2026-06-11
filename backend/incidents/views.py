from django.contrib.gis.geos import Point
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.services import broadcast_alert
from users.permissions import IsRescue

from .models import Incident
from .serializers import IncidentSerializer, SOSCreateSerializer


class IncidentListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer
    filterset_fields = ["incident_type", "status", "priority", "is_sos"]
    search_fields = ["title", "description", "address"]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user or user.is_rescue:
            return Incident.objects.all()
        return Incident.objects.filter(reporter=user)


class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user or user.is_rescue:
            return Incident.objects.all()
        return Incident.objects.filter(reporter=user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == Incident.Status.RESOLVED and not instance.resolved_at:
            instance.resolved_at = timezone.now()
            instance.save(update_fields=["resolved_at"])


class SOSView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SOSCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        incident = Incident.objects.create(
            reporter=request.user,
            incident_type=Incident.IncidentType.SOS,
            title="SOS - Urgence",
            description=data["description"],
            location=Point(data["lng"], data["lat"], srid=4326),
            people_affected=data["people_affected"],
            is_sos=True,
            priority=Incident.Priority.CRITICAL,
        )

        broadcast_alert(
            alert_type="sos",
            title="🚨 SOS Urgence",
            message=f"{request.user.get_full_name() or request.user.username} a déclenché un SOS",
            severity="critical",
            data={
                "incident_id": incident.id,
                "lat": data["lat"],
                "lng": data["lng"],
                "reporter": request.user.get_full_name() or request.user.username,
            },
            target_role="rescue",
        )
        if request.user.phone:
            try:
                from communications.services import send_sms
                send_sms(request.user.phone, "SOS ARCA-GIS confirmé. Secours en route.", "sos")
            except Exception:
                pass

        return Response(
            IncidentSerializer(incident, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class AssignIncidentView(APIView):
    permission_classes = [IsRescue]

    def post(self, request, pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response({"error": "Incident introuvable"}, status=status.HTTP_404_NOT_FOUND)

        incident.assigned_to = request.user
        incident.status = Incident.Status.ACKNOWLEDGED
        incident.save()

        broadcast_alert(
            alert_type="incident_update",
            title="Incident pris en charge",
            message=f"{request.user.get_full_name()} a pris en charge l'incident #{incident.id}",
            severity="medium",
            data={"incident_id": incident.id, "status": incident.status},
        )

        return Response(IncidentSerializer(incident).data)


class ActiveSOSListView(generics.ListAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(
            is_sos=True,
            status__in=[Incident.Status.PENDING, Incident.Status.ACKNOWLEDGED, Incident.Status.IN_PROGRESS],
        )
