from rest_framework import serializers

from .models import CarbonCredit


class CarbonCreditSerializer(serializers.ModelSerializer):
    parcel_name = serializers.CharField(source="parcel.name", read_only=True)

    class Meta:
        model = CarbonCredit
        fields = [
            "id", "parcel", "parcel_name", "co2_tons_sequestered",
            "credit_value_usd", "methodology", "verified", "period_start", "period_end",
        ]
        read_only_fields = ["id", "owner", "created_at"]
