from rest_framework import serializers

from .listings_models import CropListing


class CropListingSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.get_full_name", read_only=True)

    class Meta:
        model = CropListing
        fields = [
            "id", "seller", "seller_name", "crop_type", "quantity_kg",
            "price_per_kg", "currency", "quality_grade", "harvest_certificate",
            "region", "description", "status", "created_at",
        ]
        read_only_fields = ["id", "seller", "created_at"]

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user
        return super().create(validated_data)
