from django.contrib import admin

from .models import DeviceToken, PushNotification


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "platform", "is_active", "updated_at"]


@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "sent", "created_at"]
