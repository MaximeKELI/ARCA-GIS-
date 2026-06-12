from rest_framework import serializers

from .models import CommunityMapPoint, WMSLayer


class CommunityMapPointSerializer(serializers.ModelSerializer):
    contributor_name = serializers.CharField(source="contributor.get_full_name", read_only=True)

    class Meta:
        model = CommunityMapPoint
        fields = ["id", "contributor", "contributor_name", "name", "category", "location", "description", "verified", "created_at"]
        read_only_fields = ["id", "contributor", "verified", "created_at"]

    def create(self, validated_data):
        validated_data["contributor"] = self.context["request"].user
        return super().create(validated_data)


class WMSLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WMSLayer
        fields = ["id", "name", "source_url", "layer_name", "country", "is_active", "opacity"]
