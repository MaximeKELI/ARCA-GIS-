from rest_framework import serializers

from .models import Course, CourseProgress


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "category", "language",
            "video_url", "duration_minutes", "crop_types", "difficulty",
        ]


class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = CourseProgress
        fields = ["id", "course", "course_title", "completed", "progress_pct", "completed_at"]
        read_only_fields = ["id"]
