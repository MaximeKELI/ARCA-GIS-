from django.contrib.gis.geos import Point
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    position_lat = serializers.SerializerMethodField()
    position_lng = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "role_display", "phone", "organization",
            "country", "region", "is_available",
            "position_lat", "position_lng",
            "latitude", "longitude",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_position_lat(self, obj):
        return obj.last_position.y if obj.last_position else None

    def get_position_lng(self, obj):
        return obj.last_position.x if obj.last_position else None

    def update(self, instance, validated_data):
        lat = validated_data.pop("latitude", None)
        lng = validated_data.pop("longitude", None)
        if lat is not None and lng is not None:
            instance.last_position = Point(lng, lat, srid=4326)
        return super().update(instance, validated_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "password_confirm",
            "first_name", "last_name", "role", "phone",
            "organization", "country", "region",
        ]

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        restricted = (User.Role.ADMIN, User.Role.GOVERNMENT)
        if data.get("role") in restricted:
            raise serializers.ValidationError({"role": "Ce rôle ne peut pas être auto-assigné."})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        return User.objects.create_user(
            password=password,
            is_2fa_enabled=False,
            preferred_language="fr",
            **validated_data,
        )
