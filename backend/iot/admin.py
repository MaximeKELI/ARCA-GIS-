from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import IoTSensor, SensorReading


@admin.register(IoTSensor)
class IoTSensorAdmin(GISModelAdmin):
    list_display = ["name", "sensor_type", "device_id", "is_active", "battery_level"]


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ["sensor", "value", "unit", "recorded_at"]
