from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Parcel


class ParcelSerializer(GeoFeatureModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    crop_type_display = serializers.CharField(source="get_crop_type_display", read_only=True)
    health_status_display = serializers.CharField(source="get_health_status_display", read_only=True)

    class Meta:
        model = Parcel
        geo_field = "geometry"
        fields = [
            "id", "owner", "owner_name", "name", "crop_type", "crop_type_display",
            "geometry", "area_hectares", "health_status", "health_status_display",
            "soil_moisture", "planting_date", "expected_harvest",
            "notes", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "area_hectares", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class ParcelListSerializer(serializers.ModelSerializer):
    crop_type_display = serializers.CharField(source="get_crop_type_display", read_only=True)
    health_status_display = serializers.CharField(source="get_health_status_display", read_only=True)
    centroid_lat = serializers.SerializerMethodField()
    centroid_lng = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = [
            "id", "name", "crop_type", "crop_type_display",
            "area_hectares", "health_status", "health_status_display",
            "soil_moisture", "centroid_lat", "centroid_lng",
            "is_active", "created_at",
        ]

    def get_centroid_lat(self, obj):
        return obj.geometry.centroid.y if obj.geometry else None

    def get_centroid_lng(self, obj):
        return obj.geometry.centroid.x if obj.geometry else None
