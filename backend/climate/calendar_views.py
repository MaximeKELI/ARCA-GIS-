from datetime import datetime

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CropCalendar


class CropCalendarListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = CropCalendar.objects.all()
        crop = self.request.query_params.get("crop")
        region = self.request.query_params.get("region")
        if crop:
            qs = qs.filter(crop_type=crop)
        if region:
            qs = qs.filter(region=region)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = [{
            "crop_type": c.crop_type, "crop_name": c.crop_name, "region": c.region,
            "planting": f"{c.planting_start} → {c.planting_end}",
            "harvest": f"{c.harvest_start} → {c.harvest_end}",
            "treatments": c.treatments, "tips": c.tips,
        } for c in qs]
        return Response(data)


class CurrentSeasonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = datetime.now().strftime("%m-%d")
        active = []
        for cal in CropCalendar.objects.all():
            if cal.planting_start <= today <= cal.planting_end:
                active.append({"crop": cal.crop_name, "action": "Semis recommandé", "region": cal.region})
            elif cal.harvest_start <= today <= cal.harvest_end:
                active.append({"crop": cal.crop_name, "action": "Récolte en cours", "region": cal.region})
        return Response({"date": today, "recommendations": active})
