from rest_framework import serializers

from .models import HarvestRecord


class HarvestRecordSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source="farmer.get_full_name", read_only=True)
    parcel_name = serializers.CharField(source="parcel.name", read_only=True)

    class Meta:
        model = HarvestRecord
        fields = [
            "id", "parcel", "parcel_name", "farmer", "farmer_name",
            "crop_type", "quantity_kg", "quality_grade", "harvest_date",
            "blockchain_hash", "previous_hash", "certificate_id",
            "destination", "created_at",
        ]
        read_only_fields = ["id", "blockchain_hash", "previous_hash", "certificate_id", "created_at"]

    def create(self, validated_data):
        validated_data["farmer"] = self.context["request"].user
        return super().create(validated_data)
