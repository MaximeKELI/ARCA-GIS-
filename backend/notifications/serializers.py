from rest_framework import serializers

from .models import DeviceToken, PushNotification


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["id", "token", "platform", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        token, _ = DeviceToken.objects.update_or_create(
            token=validated_data["token"],
            defaults={
                "user": validated_data["user"],
                "platform": validated_data.get("platform", "android"),
                "is_active": True,
            },
        )
        return token


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = ["id", "title", "body", "data", "sent", "created_at"]
