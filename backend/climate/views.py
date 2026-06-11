from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdmin

from .models import ClimateEvent, WeatherReading, WeatherStation
from .serializers import ClimateEventSerializer, WeatherReadingSerializer, WeatherStationSerializer
from .services import fetch_forecast, fetch_real_weather, request_ai_analysis


class ClimateEventListCreateView(generics.ListCreateAPIView):
    serializer_class = ClimateEventSerializer
    filterset_fields = ["event_type", "severity", "country", "region", "is_active"]
    search_fields = ["title", "description", "region"]

    def get_queryset(self):
        return ClimateEvent.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class ClimateEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClimateEvent.objects.all()
    serializer_class = ClimateEventSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class NearbyClimateEventsView(generics.ListAPIView):
    serializer_class = ClimateEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")
        radius_km = float(self.request.query_params.get("radius", 100))

        if not lat or not lng:
            return ClimateEvent.objects.filter(is_active=True)

        point = Point(float(lng), float(lat), srid=4326)
        return ClimateEvent.objects.filter(
            center_point__distance_lte=(point, D(km=radius_km)),
            is_active=True,
        )


class AIAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        crop_type = request.data.get("crop_type", "maize")

        if not lat or not lng:
            return Response(
                {"error": "lat et lng sont requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = request_ai_analysis(float(lat), float(lng), crop_type)
        return Response(result)


class WeatherCurrentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        if not lat or not lng:
            return Response({"error": "lat/lng requis"}, status=400)
        weather = fetch_real_weather(float(lat), float(lng))
        if not weather:
            return Response({"error": "Météo indisponible"}, status=503)
        return Response(weather)


class WeatherForecastView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        days = int(request.query_params.get("days", 7))
        if not lat or not lng:
            return Response({"error": "lat/lng requis"}, status=400)
        return Response({"forecast": fetch_forecast(float(lat), float(lng), days)})


class WeatherStationListView(generics.ListAPIView):
    queryset = WeatherStation.objects.filter(is_active=True)
    serializer_class = WeatherStationSerializer
    permission_classes = [permissions.IsAuthenticated]


class WeatherReadingListView(generics.ListAPIView):
    serializer_class = WeatherReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        station_id = self.request.query_params.get("station")
        qs = WeatherReading.objects.all()
        if station_id:
            qs = qs.filter(station_id=station_id)
        return qs[:50]
