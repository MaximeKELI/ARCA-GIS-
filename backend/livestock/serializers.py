from rest_framework import serializers

from .models import Herd, VeterinaryAlert


class HerdSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)

    class Meta:
        model = Herd
        fields = [
            "id", "owner", "owner_name", "name", "animal_type", "count",
            "location", "pasture_area_ha", "health_status", "notes", "created_at",
        ]
        read_only_fields = ["id", "owner", "created_at"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class VeterinaryAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = VeterinaryAlert
        fields = ["id", "herd", "disease", "severity", "region", "description", "is_active", "reported_at"]
        read_only_fields = ["id", "reported_at"]
