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

        self.stdout.write("Création coopérative et sols...")
        from cooperatives.models import Cooperative
        from marketplace.services import seed_market_prices
        from soils.models import SoilZone

        coop, _ = Cooperative.objects.get_or_create(
            name="Coopérative Agricole Bouaké",
            defaults={
                "description": "Groupement de producteurs de maïs et riz",
                "country": "Côte d'Ivoire", "region": "Bouaké",
                "location": Point(-5.0300, 7.6900, srid=4326),
                "president": farmer, "total_hectares": 45.0,
            },
        )
        coop.members.add(farmer)
        coop.member_count = 1
        coop.save()

        SoilZone.objects.get_or_create(
            name="Ferralsol Bouaké Nord",
            defaults={
                "soil_type": SoilZone.SoilType.FERRALSOL,
                "geometry": Polygon([
                    (-5.050, 7.710), (-5.010, 7.710),
                    (-5.010, 7.670), (-5.050, 7.670), (-5.050, 7.710),
                ], srid=4326),
                "ph": 5.8, "organic_matter": 2.1, "texture": "argilo-sableux",
                "country": "Côte d'Ivoire", "region": "Bouaké",
            },
        )

        seed_market_prices()

        self.stdout.write("Création données v4...")
        from climate.models import CropCalendar
        from forum.models import ForumCategory, ForumPost
        from gamification.models import Badge, UserProfile
        from gamification.services import award_points
        from insurance.models import InsurancePolicy
        from marketplace.models import CropListing
        from subscriptions.models import Plan, UserSubscription
        from training.models import Course
        from iot.models import PestTrap, RiverBuoy

        for tier, name, price, parcels in [
            ("free", "Gratuit", 0, 3), ("farmer", "Agriculteur Pro", 5000, 20),
            ("coop", "Coopérative", 25000, 100),
        ]:
            Plan.objects.get_or_create(tier=tier, defaults={
                "name": name, "price_monthly": price, "max_parcels": parcels,
                "features": ["alertes", "carte", "ia"],
            })
        free_plan = Plan.objects.get(tier="free")
        UserSubscription.objects.get_or_create(user=farmer, defaults={"plan": free_plan})

        CropCalendar.objects.get_or_create(crop_type="maize", region="Bouaké", defaults={
            "crop_name": "Maïs", "planting_start": "04-01", "planting_end": "05-15",
            "harvest_start": "08-01", "harvest_end": "09-30",
            "treatments": ["herbicide J+15", "engrais NPK J+30"],
            "tips": "Semis après premières pluies.",
        })

        cat, _ = ForumCategory.objects.get_or_create(slug="bouake", defaults={
            "name": "Bouaké", "region": "Bouaké", "description": "Échanges locaux",
        })
        ForumPost.objects.get_or_create(title="Meilleur moment pour semer le maïs ?", defaults={
            "author": farmer, "category": cat,
            "content": "Quand commencez-vous les semis cette année ?",
        })

        Course.objects.get_or_create(title="Irrigation efficace", defaults={
            "description": "Techniques d'arrosage économes en eau",
            "category": "water", "language": "fr", "duration_minutes": 15,
            "crop_types": ["maize", "rice"], "difficulty": "beginner", "is_published": True,
        })

        Badge.objects.get_or_create(slug="first_parcel", defaults={
            "name": "Première parcelle", "description": "Enregistrer sa première parcelle",
            "icon": "🌱", "points": 50,
        })
        profile, _ = UserProfile.objects.get_or_create(user=farmer)
        award_points(farmer, "login")

        from datetime import date
        first_parcel = Parcel.objects.first()
        if first_parcel:
            InsurancePolicy.objects.get_or_create(
                farmer=farmer, parcel=first_parcel, policy_type="drought",
                defaults={
                    "coverage_amount": 500000, "premium": 15000,
                    "start_date": date.today(), "end_date": date(2026, 12, 31),
                    "trigger_threshold": {"rainfall_mm": 50, "days": 30},
                },
            )

        CropListing.objects.get_or_create(
            seller=farmer, crop_type="maize", region="Bouaké", defaults={
                "quantity_kg": 500, "price_per_kg": 250, "quality_grade": "A",
                "description": "Maïs jaune, récolte 2024",
            },
        )

        RiverBuoy.objects.get_or_create(device_id="BUOY-001", defaults={
            "name": "Bouée Bandama", "river_name": "Bandama",
            "location": Point(-5.050, 7.700, srid=4326), "alert_level_m": 4.0,
        })
        PestTrap.objects.get_or_create(device_id="TRAP-001", defaults={
            "name": "Piège Maïs Nord", "location": Point(-5.033, 7.693, srid=4326),
            "parcel": Parcel.objects.first(),
        })

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès!"))
        self.stdout.write("Comptes: admin/admin1234, kouassi/farmer1234, secours/rescue1234")
