from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from .models import Incident


class DispatchNearestRescueView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response({"error": "Incident introuvable"}, status=404)

        if not incident.location:
            return Response({"error": "Pas de localisation"}, status=400)

        rescuers = User.objects.filter(
            role=User.Role.RESCUE, is_available=True, last_position__isnull=False,
        ).annotate(distance=Distance("last_position", incident.location)).order_by("distance")[:3]

        assigned = []
        for r in rescuers:
            assigned.append({
                "id": r.id, "name": r.get_full_name(),
                "organization": r.organization,
                "distance_km": round(r.distance.km, 1) if r.distance else None,
            })

        incident.status = Incident.Status.ACKNOWLEDGED
        incident.save(update_fields=["status"])

        return Response({"incident_id": pk, "assigned_rescuers": assigned})


class EvacuationChecklistView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        disaster = request.query_params.get("type", "flood")
        checklists = {
            "flood": [
                "Monter en hauteur immédiatement",
                "Couper l'électricité",
                "Emporter documents et médicaments",
                "Signaler sa position via SOS ARCA-GIS",
                "Éviter les cours d'eau et ponts",
            ],
            "drought": [
                "Réduire consommation eau de 50%",
                "Protéger bétail — déplacer vers point d'eau",
                "Stocker nourriture et fourrage",
                "Activer irrigation de secours",
            ],
            "fire": [
                "Évacuer dans direction du vent opposé",
                "Couvrir nez et bouche",
                "Laisser portes ouvertes pour secours",
                "Signaler position GPS",
            ],
        }
        return Response({"disaster_type": disaster, "steps": checklists.get(disaster, checklists["flood"])})
