from rest_framework import serializers

from .models import Badge, PointEvent, UserProfile


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["slug", "name", "description", "icon", "points"]


class UserProfileSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["total_points", "level", "streak_days", "badges", "username"]


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["username", "full_name", "total_points", "level"]
