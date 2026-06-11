from rest_framework import serializers

from .models import DroneMission


class DroneMissionSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source="operator.get_full_name", read_only=True)
    mission_type_display = serializers.CharField(source="get_mission_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = DroneMission
        fields = [
            "id", "operator", "operator_name", "parcel", "mission_type",
            "mission_type_display", "status", "status_display",
            "flight_path", "coverage_area", "altitude_m",
            "scheduled_at", "completed_at", "notes", "created_at",
        ]
        read_only_fields = ["id", "operator", "created_at"]

    def create(self, validated_data):
        validated_data["operator"] = self.context["request"].user
        return super().create(validated_data)
