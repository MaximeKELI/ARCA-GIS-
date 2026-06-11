from rest_framework import serializers

from .models import IoTSensor, SensorReading


class IoTSensorSerializer(serializers.ModelSerializer):
    sensor_type_display = serializers.CharField(source="get_sensor_type_display", read_only=True)
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()
    latest_value = serializers.SerializerMethodField()

    class Meta:
        model = IoTSensor
        fields = [
            "id", "name", "sensor_type", "sensor_type_display", "device_id",
            "location", "lat", "lng", "parcel", "is_active",
            "battery_level", "last_seen", "latest_value", "created_at",
        ]

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x

    def get_latest_value(self, obj):
        reading = obj.readings.first()
        return reading.value if reading else None


class SensorReadingSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField(source="sensor.name", read_only=True)

    class Meta:
        model = SensorReading
        fields = ["id", "sensor", "sensor_name", "value", "unit", "recorded_at"]
        read_only_fields = ["id"]
