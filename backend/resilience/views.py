import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EarlyWarningAlert, RadioHFStation, RefugeCenter


class RefugeListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = RefugeCenter.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        return Response([{
            "id": r.id, "name": r.name, "type": r.center_type,
            "location": {"lat": r.location.y, "lng": r.location.x},
            "capacity": r.capacity, "region": r.region,
        } for r in self.get_queryset()])


class EarlyWarningListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EarlyWarningAlert.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        return Response([{
            "hazard": a.hazard_type, "level": a.level, "title": a.title,
            "region": a.region, "forecast_days": a.forecast_days,
        } for a in self.get_queryset()])


class DroughtEWSView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        region = request.query_params.get("region", "Bouaké")
        try:
            resp = requests.post(f"{settings.AI_MODULE_URL}/drought-forecast",
                                 json={"region": region, "days": 90}, timeout=10)
            data = resp.json()
            if resp.status_code >= 400 or "risk_level" not in data:
                raise requests.RequestException()
            return Response(data)
        except requests.RequestException:
            return Response({
                "region": region, "risk_level": "moderate", "forecast_days": 90,
                "probability_drought": 0.45,
                "recommendations": ["Réserver eau", "Semis cultures résistantes"],
                "source": "fallback",
            })


class FloodSimulationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        rainfall_mm = float(request.data.get("rainfall_mm", 100))
        elevation_m = float(request.data.get("elevation_m", 200))
        affected_pct = min(95, max(0, (rainfall_mm - 50) / 2 * (1 - elevation_m / 500)))
        return Response({
            "rainfall_mm": rainfall_mm,
            "elevation_m": elevation_m,
            "flood_risk_pct": round(affected_pct, 1),
            "evacuation_recommended": affected_pct > 60,
            "affected_zones": ["plaine basse", "berges"] if affected_pct > 40 else [],
        })


class RadioHFListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = RadioHFStation.objects.filter(is_operational=True)

    def list(self, request, *args, **kwargs):
        return Response([{
            "name": s.name, "frequency": s.frequency, "region": s.region,
        } for s in self.get_queryset()])
