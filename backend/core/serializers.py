from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import AuditLog, GeofenceZone, OfflineSyncQueue


class GeofenceZoneSerializer(GeoFeatureModelSerializer):
    zone_type_display = serializers.CharField(source="get_zone_type_display", read_only=True)

    class Meta:
        model = GeofenceZone
        geo_field = "geometry"
        fields = [
            "id", "name", "zone_type", "zone_type_display", "geometry",
            "description", "alert_on_enter", "alert_on_exit", "is_active", "created_at",
        ]


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True, default=None)

    class Meta:
        model = AuditLog
        fields = ["id", "user", "username", "action", "resource", "resource_id",
                  "ip_address", "details", "created_at"]


class OfflineSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineSyncQueue
        fields = ["id", "action_type", "payload", "synced", "created_at"]
        read_only_fields = ["id", "synced", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
