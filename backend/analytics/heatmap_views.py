from django.db.models import Avg
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from parcels.models import Parcel


class YieldHeatmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        region = request.query_params.get("region")
        parcels = Parcel.objects.filter(is_active=True)
        if region:
            parcels = parcels.filter(owner__region=region)

        cells = []
        for p in parcels:
            if p.geometry:
                centroid = p.geometry.centroid
                cells.append({
                    "lat": centroid.y, "lng": centroid.x,
                    "health": p.health_status,
                    "moisture": p.soil_moisture,
                    "crop": p.crop_type,
                    "intensity": {"good": 0.8, "moderate": 0.5, "poor": 0.2, "critical": 0.1}.get(p.health_status, 0.5),
                })
        return Response({
            "region": region or "all",
            "cell_count": len(cells),
            "avg_moisture": parcels.aggregate(a=Avg("soil_moisture"))["a"],
            "cells": cells[:200],
        })
