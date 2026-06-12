from rest_framework import serializers

from .models import ShipmentRequest, Transporter


class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = ["id", "name", "phone", "region", "vehicle_type", "capacity_kg", "price_per_km", "rating", "is_available"]


class ShipmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentRequest
        fields = [
            "id", "farmer", "transporter", "crop_type", "quantity_kg",
            "origin", "destination", "distance_km", "quoted_price", "status", "created_at",
        ]
        read_only_fields = ["id", "farmer", "quoted_price", "created_at"]

    def create(self, validated_data):
        validated_data["farmer"] = self.context["request"].user
        return super().create(validated_data)
