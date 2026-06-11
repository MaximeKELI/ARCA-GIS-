from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.services import broadcast_alert

from .models import PestTrap, RiverBuoy


class BuoyIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        level = request.data.get("water_level_m")
        try:
            buoy = RiverBuoy.objects.get(device_id=device_id)
        except RiverBuoy.DoesNotExist:
            return Response({"error": "Bouée inconnue"}, status=404)
        buoy.water_level_m = float(level)
        buoy.last_reading_at = timezone.now()
        buoy.save()
        if buoy.water_level_m >= buoy.alert_level_m:
            broadcast_alert("climate", f"⚠️ Niveau eau élevé — {buoy.river_name}",
                            f"Niveau: {level}m (seuil: {buoy.alert_level_m}m)", "high",
                            {"device_id": device_id, "level": level}, "rescue")
        return Response({"status": "ok", "level": level})


class PestTrapIngestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        count = request.data.get("pest_count", 0)
        try:
            trap = PestTrap.objects.get(device_id=device_id)
        except PestTrap.DoesNotExist:
            return Response({"error": "Piège inconnu"}, status=404)
        trap.pest_count = int(count)
        if count > 50:
            try:
                import requests
                from django.conf import settings
                resp = requests.post(f"{settings.AI_MODULE_URL}/disease-detect/pest",
                                     json={"pest_count": count, "crop_type": "maize"}, timeout=5)
                trap.ai_diagnosis = resp.json()
            except Exception:
                trap.ai_diagnosis = {"risk": "high", "recommendation": "Traitement préventif"}
            broadcast_alert("crop", "Ravageurs détectés", f"{count} insectes au piège {trap.name}",
                            "medium", {"trap_id": trap.id, "count": count}, "farmer")
        trap.save()
        return Response({"status": "ok", "count": count, "diagnosis": trap.ai_diagnosis})
