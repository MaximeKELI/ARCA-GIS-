from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Incident


class IncidentSerializer(GeoFeatureModelSerializer):
    reporter_name = serializers.CharField(source="reporter.get_full_name", read_only=True)
    assigned_to_name = serializers.CharField(
        source="assigned_to.get_full_name",
        read_only=True,
        default=None,
    )
    incident_type_display = serializers.CharField(source="get_incident_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        geo_field = "location"
        fields = [
            "id", "reporter", "reporter_name", "assigned_to", "assigned_to_name",
            "incident_type", "incident_type_display", "status", "status_display",
            "priority", "priority_display", "title", "description",
            "location", "lat", "lng", "address", "photo",
            "people_affected", "is_sos", "resolved_at",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "reporter", "is_sos", "created_at", "updated_at"]

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x

    def create(self, validated_data):
        validated_data["reporter"] = self.context["request"].user
        return super().create(validated_data)


class SOSCreateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    description = serializers.CharField(required=False, default="SOS - Urgence signalée")
    people_affected = serializers.IntegerField(required=False, default=1)
