from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import ClimateEvent, WeatherReading, WeatherStation


class ClimateEventSerializer(GeoFeatureModelSerializer):
    event_type_display = serializers.CharField(source="get_event_type_display", read_only=True)
    severity_display = serializers.CharField(source="get_severity_display", read_only=True)
    center_lat = serializers.SerializerMethodField()
    center_lng = serializers.SerializerMethodField()

    class Meta:
        model = ClimateEvent
        geo_field = "geometry"
        fields = [
            "id", "event_type", "event_type_display", "severity", "severity_display",
            "title", "description", "geometry", "center_point",
            "center_lat", "center_lng", "affected_area_km2",
            "temperature", "rainfall_mm", "humidity", "wind_speed",
            "country", "region", "is_active",
            "ai_confidence", "ai_recommendation",
            "started_at", "ended_at", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_center_lat(self, obj):
        return obj.center_point.y if obj.center_point else None

    def get_center_lng(self, obj):
        return obj.center_point.x if obj.center_point else None


class WeatherStationSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = WeatherStation
        fields = ["id", "name", "location", "lat", "lng", "country", "region",
                  "elevation_m", "is_active"]

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x


class WeatherReadingSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source="station.name", read_only=True)

    class Meta:
        model = WeatherReading
        fields = [
            "id", "station", "station_name", "temperature", "rainfall_mm",
            "humidity", "wind_speed", "soil_moisture", "recorded_at",
        ]
        read_only_fields = ["id"]
