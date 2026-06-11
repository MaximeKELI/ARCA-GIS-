from django.contrib.gis.db import models


class IoTSensor(models.Model):
    class SensorType(models.TextChoices):
        SOIL_MOISTURE = "soil_moisture", "Humidité sol"
        RAINFALL = "rainfall", "Pluviomètre"
        TEMPERATURE = "temperature", "Température"
        HUMIDITY = "humidity", "Humidité air"
        WATER_LEVEL = "water_level", "Niveau d'eau"

    name = models.CharField(max_length=200)
    sensor_type = models.CharField(max_length=20, choices=SensorType.choices)
    device_id = models.CharField(max_length=100, unique=True)
    location = models.PointField(srid=4326)
    parcel = models.ForeignKey(
        "parcels.Parcel", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    battery_level = models.FloatField(default=100.0)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class SensorReading(models.Model):
    sensor = models.ForeignKey(IoTSensor, on_delete=models.CASCADE, related_name="readings")
    value = models.FloatField()
    unit = models.CharField(max_length=20, default="%")
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]


class RiverBuoy(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    river_name = models.CharField(max_length=200)
    water_level_m = models.FloatField(default=0.0)
    alert_level_m = models.FloatField(default=3.0)
    is_active = models.BooleanField(default=True)
    last_reading_at = models.DateTimeField(null=True, blank=True)


class PestTrap(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    parcel = models.ForeignKey("parcels.Parcel", on_delete=models.SET_NULL, null=True, blank=True)
    pest_count = models.PositiveIntegerField(default=0)
    last_image = models.ImageField(upload_to="pest_traps/", blank=True)
    ai_diagnosis = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
