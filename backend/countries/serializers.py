from rest_framework import serializers

from .models import CountryConfig


class CountryConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryConfig
        fields = ["code", "name", "currency", "timezone", "default_language", "emergency_number", "settings"]
