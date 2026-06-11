from datetime import timedelta

from django.contrib.gis.geos import Point, Polygon  # Polygon used for geofences
from django.core.management.base import BaseCommand
from django.utils import timezone

from climate.models import ClimateEvent, WeatherReading, WeatherStation
from parcels.models import Parcel
from users.models import User


class Command(BaseCommand):
    help = "Initialise les données de démonstration ARCA-GIS"

    def handle(self, *args, **options):
        self.stdout.write("Création des utilisateurs...")
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@arca-gis.africa",
                "first_name": "Admin",
                "last_name": "ARCA",
                "role": User.Role.ADMIN,
                "country": "Côte d'Ivoire",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("admin1234")
        admin.save()

        farmer, _ = User.objects.get_or_create(
            username="kouassi",
            defaults={
                "email": "kouassi@example.ci",
                "first_name": "Jean",
                "last_name": "Kouassi",
                "role": User.Role.FARMER,
                "phone": "+2250700000001",
                "country": "Côte d'Ivoire",
                "region": "Bouaké",
                "last_position": Point(-5.0300, 7.6900, srid=4326),
            },
        )
        farmer.set_password("farmer1234")
        farmer.save()

        rescue, _ = User.objects.get_or_create(
            username="secours",
            defaults={
                "email": "secours@arca-gis.africa",
                "first_name": "Aminata",
                "last_name": "Traoré",
                "role": User.Role.RESCUE,
                "phone": "+2250700000002",
                "organization": "Protection Civile CI",
                "country": "Côte d'Ivoire",
                "region": "Abidjan",
                "last_position": Point(-4.0083, 5.3600, srid=4326),
            },
        )
        rescue.set_password("rescue1234")
        rescue.save()

        self.stdout.write("Création des parcelles...")
        parcels_data = [
            {
                "name": "Champ Maïs Nord",
                "crop_type": Parcel.CropType.MAIZE,
                "coords": [(-5.035, 7.695), (-5.030, 7.695), (-5.030, 7.690), (-5.035, 7.690), (-5.035, 7.695)],
                "health": Parcel.HealthStatus.GOOD,
                "moisture": 55.0,
            },
            {
                "name": "Rizière Sud",
                "crop_type": Parcel.CropType.RICE,
                "coords": [(-5.028, 7.685), (-5.023, 7.685), (-5.023, 7.680), (-5.028, 7.680), (-5.028, 7.685)],
                "health": Parcel.HealthStatus.MODERATE,
                "moisture": 72.0,
            },
            {
                "name": "Plantation Cacao",
                "crop_type": Parcel.CropType.COCOA,
                "coords": [(-5.040, 7.700), (-5.035, 7.700), (-5.035, 7.695), (-5.040, 7.695), (-5.040, 7.700)],
                "health": Parcel.HealthStatus.EXCELLENT,
                "moisture": 68.0,
            },
        ]

        for p in parcels_data:
            Parcel.objects.get_or_create(
                name=p["name"],
                owner=farmer,
                defaults={
                    "crop_type": p["crop_type"],
                    "geometry": Polygon(p["coords"], srid=4326),
                    "health_status": p["health"],
                    "soil_moisture": p["moisture"],
                    "planting_date": timezone.now().date() - timedelta(days=60),
                },
            )

        self.stdout.write("Création des événements climatiques...")
        ClimateEvent.objects.get_or_create(
            title="Sécheresse région Bouaké",
            defaults={
                "event_type": ClimateEvent.EventType.DROUGHT,
                "severity": ClimateEvent.Severity.HIGH,
                "description": "Déficit pluviométrique important affectant les cultures de maïs et arachide.",
                "center_point": Point(-5.0300, 7.6900, srid=4326),
                "temperature": 36.5,
                "rainfall_mm": 5.0,
                "humidity": 35.0,
                "country": "Côte d'Ivoire",
                "region": "Bouaké",
                "ai_confidence": 0.82,
                "ai_recommendation": "Irrigation d'appoint recommandée. Réduire la densité de semis de 20%.",
                "started_at": timezone.now() - timedelta(days=5),
            },
        )

        ClimateEvent.objects.get_or_create(
            title="Risque inondation Abidjan",
            defaults={
                "event_type": ClimateEvent.EventType.FLOOD,
                "severity": ClimateEvent.Severity.MEDIUM,
                "description": "Fortes pluies prévues dans la région d'Abidjan et environs.",
                "center_point": Point(-4.0083, 5.3600, srid=4326),
                "temperature": 28.0,
                "rainfall_mm": 120.0,
                "humidity": 88.0,
                "country": "Côte d'Ivoire",
                "region": "Abidjan",
                "ai_confidence": 0.75,
                "ai_recommendation": "Évacuer les zones basses. Protéger les stocks de semences.",
                "started_at": timezone.now() - timedelta(days=1),
            },
        )

        self.stdout.write("Création des stations météo...")
        station, _ = WeatherStation.objects.get_or_create(
            name="Station Bouaké Centre",
            defaults={
                "location": Point(-5.0300, 7.6900, srid=4326),
                "country": "Côte d'Ivoire",
                "region": "Bouaké",
                "elevation_m": 295,
            },
        )

        WeatherReading.objects.get_or_create(
            station=station,
            recorded_at=timezone.now(),
            defaults={
                "temperature": 33.5,
                "rainfall_mm": 2.0,
                "humidity": 42.0,
                "wind_speed": 12.0,
                "soil_moisture": 38.0,
            },
        )

        self.stdout.write("Création des capteurs IoT...")
        from iot.models import IoTSensor, SensorReading
        from core.models import GeofenceZone

        sensor, _ = IoTSensor.objects.get_or_create(
            device_id="IOT-BOUAKE-001",
            defaults={
                "name": "Capteur Sol Bouaké",
                "sensor_type": IoTSensor.SensorType.SOIL_MOISTURE,
                "location": Point(-5.0320, 7.6920, srid=4326),
                "battery_level": 87.0,
                "last_seen": timezone.now(),
            },
        )
        SensorReading.objects.get_or_create(
            sensor=sensor,
            recorded_at=timezone.now(),
            defaults={"value": 38.0, "unit": "%"},
        )

        self.stdout.write("Création des zones géofencing...")
        GeofenceZone.objects.get_or_create(
            name="Zone sécheresse Bouaké",
            defaults={
                "zone_type": GeofenceZone.ZoneType.RISK,
                "geometry": Polygon([
                    (-5.045, 7.700), (-5.020, 7.700),
                    (-5.020, 7.675), (-5.045, 7.675), (-5.045, 7.700),
                ], srid=4326),
                "description": "Zone à risque sécheresse — irrigation recommandée",
                "alert_on_enter": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès!"))
        self.stdout.write("Comptes: admin/admin1234, kouassi/farmer1234, secours/rescue1234")
