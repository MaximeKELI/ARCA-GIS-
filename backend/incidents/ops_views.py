from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Incident
from .ops_models import InterventionLog, RescueVolunteer


class VolunteerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = RescueVolunteer.objects.filter(is_available=True)
        return Response([{
            "user": v.user.get_full_name(), "skills": v.skills,
            "vehicle": v.vehicle_type, "region": v.region,
        } for v in qs])

    def post(self, request):
        v, _ = RescueVolunteer.objects.update_or_create(
            user=request.user,
            defaults={
                "skills": request.data.get("skills", []),
                "vehicle_type": request.data.get("vehicle_type", ""),
                "region": request.data.get("region", request.user.region),
            },
        )
        return Response({"id": v.id}, status=201)


class InterventionLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        logs = InterventionLog.objects.filter(incident_id=pk)
        return Response([{"note": l.note, "status": l.status_change, "at": l.created_at.isoformat()} for l in logs])

    def post(self, request, pk):
        log = InterventionLog.objects.create(
            incident_id=pk, author=request.user,
            note=request.data.get("note", ""),
            status_change=request.data.get("status_change", ""),
        )
        if request.data.get("status"):
            Incident.objects.filter(pk=pk).update(status=request.data["status"])
        return Response({"id": log.id}, status=201)


class IncidentSLAView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            inc = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response({"error": "Introuvable"}, status=404)
        elapsed = (timezone.now() - inc.created_at).total_seconds() / 60
        sla_met = inc.status == "resolved" and elapsed < 120
        return Response({
            "incident_id": pk, "status": inc.status,
            "elapsed_minutes": round(elapsed, 1),
            "sla_target_minutes": 120, "sla_met": sla_met,
        })
