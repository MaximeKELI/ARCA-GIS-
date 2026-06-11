from django.contrib import admin

from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["title", "alert_type", "severity", "is_read", "is_broadcast", "created_at"]
    list_filter = ["alert_type", "severity", "is_read", "is_broadcast"]
