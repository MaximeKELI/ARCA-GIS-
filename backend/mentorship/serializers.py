from rest_framework import serializers

from .models import Mentorship, MentorshipSession


class MentorshipSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source="mentor.get_full_name", read_only=True)
    mentee_name = serializers.CharField(source="mentee.get_full_name", read_only=True)

    class Meta:
        model = Mentorship
        fields = [
            "id", "mentor", "mentor_name", "mentee", "mentee_name",
            "status", "focus_crop", "notes", "started_at",
        ]
        read_only_fields = ["id", "started_at"]


class MentorshipSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipSession
        fields = ["id", "mentorship", "topic", "notes", "recommendations", "scheduled_at", "completed"]
