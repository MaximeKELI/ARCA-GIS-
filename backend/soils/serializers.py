from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import SoilZone


class SoilZoneSerializer(GeoFeatureModelSerializer):
    soil_type_display = serializers.CharField(source="get_soil_type_display", read_only=True)

    class Meta:
        model = SoilZone
        geo_field = "geometry"
        fields = [
            "id", "name", "soil_type", "soil_type_display", "geometry",
            "ph", "organic_matter", "texture", "suitability",
            "country", "region", "source",
        ]
