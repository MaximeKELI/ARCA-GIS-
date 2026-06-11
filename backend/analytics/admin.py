from django.contrib import admin

from .models import AnalyticsSnapshot, CropHistory


@admin.register(CropHistory)
class CropHistoryAdmin(admin.ModelAdmin):
    list_display = ["parcel", "health_status", "soil_moisture", "ndvi_score", "recorded_at"]


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ["snapshot_type", "region", "country", "recorded_at"]
