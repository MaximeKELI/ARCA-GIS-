from django.contrib import admin

from .models import Course, CourseProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "language", "duration_minutes"]


admin.site.register(CourseProgress)
