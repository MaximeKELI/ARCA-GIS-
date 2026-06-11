from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    provider_display = serializers.CharField(source="get_provider_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "provider", "provider_display", "amount", "currency",
            "phone", "description", "reference", "status", "status_display", "created_at",
        ]
        read_only_fields = ["id", "reference", "status", "created_at"]
