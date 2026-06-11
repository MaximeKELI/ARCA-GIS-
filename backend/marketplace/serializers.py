from rest_framework import serializers

from .models import MarketPrice


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = [
            "id", "crop_type", "crop_name", "country", "region",
            "market_name", "price_per_kg", "currency", "trend",
            "recorded_at", "source",
        ]
