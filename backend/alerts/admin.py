from django.contrib import admin

from .models import Alert
from .rule_models import AlertRule, NotificationPreference


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["title", "alert_type", "severity", "is_read", "is_broadcast", "created_at"]
    list_filter = ["alert_type", "severity", "is_read", "is_broadcast"]


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "metric", "threshold", "is_active"]


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user", "climate", "crop", "sos", "market"]
