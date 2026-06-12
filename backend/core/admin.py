from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import AuditLog, GeofenceZone, OfflineSyncQueue
from .bookmark_models import Bookmark


@admin.register(GeofenceZone)
class GeofenceZoneAdmin(GISModelAdmin):
    list_display = ["name", "zone_type", "is_active"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["action", "user", "ip_address", "created_at"]
    list_filter = ["action"]


@admin.register(OfflineSyncQueue)
class OfflineSyncQueueAdmin(admin.ModelAdmin):
    list_display = ["user", "action_type", "synced", "created_at"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "resource_type", "resource_id", "label"]
