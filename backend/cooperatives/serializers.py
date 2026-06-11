from rest_framework import serializers

from .models import Cooperative


class CooperativeSerializer(serializers.ModelSerializer):
    president_name = serializers.CharField(source="president.get_full_name", read_only=True, default=None)

    class Meta:
        model = Cooperative
        fields = [
            "id", "name", "description", "country", "region", "location",
            "president", "president_name", "member_count", "total_hectares",
            "is_active", "created_at",
        ]
        read_only_fields = ["id", "member_count", "created_at"]
