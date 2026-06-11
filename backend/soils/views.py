from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SoilZone
from .serializers import SoilZoneSerializer
from .services import get_soil_at_location


class SoilZoneListView(generics.ListAPIView):
    queryset = SoilZone.objects.all()
    serializer_class = SoilZoneSerializer
    permission_classes = [permissions.IsAuthenticated]


class SoilAtLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        if not lat or not lng:
            return Response({"error": "lat/lng requis"}, status=400)
        result = get_soil_at_location(float(lat), float(lng))
        if not result:
            return Response({"message": "Aucune donnée sol à cette position"}, status=404)
        return Response(result)
