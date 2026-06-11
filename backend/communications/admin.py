from django.contrib import admin

from .models import RadioBroadcast, SMSLog


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ["phone", "message_type", "status", "provider", "created_at"]


@admin.register(RadioBroadcast)
class RadioBroadcastAdmin(admin.ModelAdmin):
    list_display = ["station_name", "region", "alert_type", "is_broadcast", "created_at"]
