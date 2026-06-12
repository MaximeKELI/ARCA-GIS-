from rest_framework import serializers

from .models import WaterPoint, WaterQuota


class WaterPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterPoint
        fields = [
            "id", "name", "point_type", "location", "region",
            "capacity_m3", "current_level_pct", "is_functional", "community_managed",
        ]


class WaterQuotaSerializer(serializers.ModelSerializer):
    water_point_name = serializers.CharField(source="water_point.name", read_only=True)

    class Meta:
        model = WaterQuota
        fields = ["id", "water_point", "water_point_name", "user", "daily_liters", "used_today_liters", "crop_type"]
