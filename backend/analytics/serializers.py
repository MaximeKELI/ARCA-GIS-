from rest_framework import serializers

from .models import AnalyticsSnapshot, CropHistory


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsSnapshot
        fields = ["id", "snapshot_type", "region", "country", "data", "recorded_at"]


class CropHistorySerializer(serializers.ModelSerializer):
    parcel_name = serializers.CharField(source="parcel.name", read_only=True)

    class Meta:
        model = CropHistory
        fields = [
            "id", "parcel", "parcel_name", "health_status", "soil_moisture",
            "temperature", "rainfall_mm", "ndvi_score", "notes", "recorded_at",
        ]
