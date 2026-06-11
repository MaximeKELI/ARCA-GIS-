from rest_framework import serializers

from .models import PartnerAPIKey


class PartnerKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerAPIKey
        fields = ["id", "name", "partner_type", "api_key", "is_active", "rate_limit", "created_at"]
        read_only_fields = ["id", "api_key", "created_at"]
