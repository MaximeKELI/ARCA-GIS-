from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import ClimateEvent, WeatherReading, WeatherStation


@admin.register(ClimateEvent)
class ClimateEventAdmin(GISModelAdmin):
    list_display = ["title", "event_type", "severity", "country", "is_active", "started_at"]
    list_filter = ["event_type", "severity", "country", "is_active"]


@admin.register(WeatherStation)
class WeatherStationAdmin(GISModelAdmin):
    list_display = ["name", "country", "region", "is_active"]


@admin.register(WeatherReading)
class WeatherReadingAdmin(admin.ModelAdmin):
    list_display = ["station", "temperature", "rainfall_mm", "humidity", "recorded_at"]
    list_filter = ["station"]
