from django.contrib import admin

from .models import Course, CourseProgress
from .quiz_models import Quiz, QuizAttempt, QuizQuestion, TrainingCertificate


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "language", "duration_minutes"]


admin.site.register(CourseProgress)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "pass_score"]


admin.site.register(QuizQuestion)
admin.site.register(QuizAttempt)


@admin.register(TrainingCertificate)
class TrainingCertificateAdmin(admin.ModelAdmin):
    list_display = ["certificate_id", "user", "course", "issued_at"]
