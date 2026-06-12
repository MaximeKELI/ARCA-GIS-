from django.contrib.gis.db import models


class ClimateEvent(models.Model):
    class EventType(models.TextChoices):
        DROUGHT = "drought", "Sécheresse"
        FLOOD = "flood", "Inondation"
        HEATWAVE = "heatwave", "Canicule"
        STORM = "storm", "Tempête"
        HAIL = "hail", "Grêle"
        PEST = "pest", "Ravageurs"
        DISEASE = "disease", "Maladie des cultures"

    class Severity(models.TextChoices):
        LOW = "low", "Faible"
        MEDIUM = "medium", "Moyen"
        HIGH = "high", "Élevé"
        CRITICAL = "critical", "Critique"

    event_type = models.CharField(max_length=20, choices=EventType.choices)
    severity = models.CharField(max_length=20, choices=Severity.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    geometry = models.PolygonField(srid=4326, null=True, blank=True)
    center_point = models.PointField(srid=4326)
    affected_area_km2 = models.FloatField(default=0.0)
    temperature = models.FloatField(null=True, blank=True, help_text="°C")
    rainfall_mm = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True, help_text="%")
    wind_speed = models.FloatField(null=True, blank=True, help_text="km/h")
    country = models.CharField(max_length=100, default="Côte d'Ivoire")
    region = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    ai_confidence = models.FloatField(default=0.0, help_text="Score IA 0-1")
    ai_recommendation = models.TextField(blank=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"


class WeatherStation(models.Model):
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    elevation_m = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WeatherReading(models.Model):
    station = models.ForeignKey(
        WeatherStation,
        on_delete=models.CASCADE,
        related_name="readings",
    )
    temperature = models.FloatField(help_text="°C")
    rainfall_mm = models.FloatField(default=0.0)
    humidity = models.FloatField(help_text="%")
    wind_speed = models.FloatField(default=0.0, help_text="km/h")
    soil_moisture = models.FloatField(null=True, blank=True, help_text="%")
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.station.name} @ {self.recorded_at}"


class CropCalendar(models.Model):
    crop_type = models.CharField(max_length=50)
    crop_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Côte d'Ivoire")
    planting_start = models.CharField(max_length=20, help_text="MM-DD")
    planting_end = models.CharField(max_length=20)
    harvest_start = models.CharField(max_length=20)
    harvest_end = models.CharField(max_length=20)
    treatments = models.JSONField(default=list)
    tips = models.TextField(blank=True)

    class Meta:
        ordering = ["crop_type", "region"]
        unique_together = ["crop_type", "region"]


from .phytosanitary_models import PhytosanitaryTreatment  # noqa: E402, F401
from .community_models import CommunityWeatherReport  # noqa: E402, F401
