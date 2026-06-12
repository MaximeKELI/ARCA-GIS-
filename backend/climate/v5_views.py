import requests
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .community_models import CommunityWeatherReport
from .phytosanitary_models import PhytosanitaryTreatment


class PhytosanitaryCalendarView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = PhytosanitaryTreatment.objects.all()
        crop = self.request.query_params.get("crop")
        if crop:
            qs = qs.filter(crop_type=crop)
        return qs

    def list(self, request, *args, **kwargs):
        data = [{
            "crop_type": t.crop_type, "week": t.week_number,
            "treatment": t.treatment_name, "product": t.product,
            "dosage": t.dosage, "target": t.target_pest, "notes": t.notes,
        } for t in self.get_queryset()]
        return Response(data)


class CommunityWeatherView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        region = self.request.query_params.get("region")
        qs = CommunityWeatherReport.objects.all()
        if region:
            qs = qs.filter(region=region)
        return qs[:50]

    def list(self, request, *args, **kwargs):
        data = [{
            "region": r.region, "temperature": r.temperature,
            "rainfall_mm": r.rainfall_mm, "observations": r.observations,
            "reported_at": r.reported_at.isoformat(),
        } for r in self.get_queryset()]
        return Response(data)

    def create(self, request, *args, **kwargs):
        report = CommunityWeatherReport.objects.create(
            reporter=request.user,
            region=request.data.get("region", request.user.region),
            temperature=request.data.get("temperature"),
            rainfall_mm=request.data.get("rainfall_mm"),
            wind_strength=request.data.get("wind_strength", ""),
            observations=request.data.get("observations", ""),
        )
        return Response({"id": report.id, "status": "recorded"}, status=201)


class WildfireFIRMSView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get("lat", "7.69")
        lng = request.query_params.get("lng", "-5.03")
        radius = request.query_params.get("radius", "50")
        api_key = getattr(settings, "NASA_FIRMS_API_KEY", "")
        if api_key:
            try:
                url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/VIIRS_SNPP_NRT/{lng},{lat},{radius}/1"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    lines = resp.text.strip().split("\n")
                    fires = [dict(zip(lines[0].split(","), l.split(","))) for l in lines[1:6] if l]
                    return Response({"source": "nasa_firms", "count": len(fires), "fires": fires})
            except requests.RequestException:
                pass
        return Response({
            "source": "simulated", "count": 0, "fires": [],
            "note": "Configurer NASA_FIRMS_API_KEY pour données réelles",
        })
