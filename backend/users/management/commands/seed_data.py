from datetime import date, timedelta

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

        self.stdout.write("Création données v5...")
        from carbon.models import CarbonCredit
        from climate.phytosanitary_models import PhytosanitaryTreatment
        from countries.models import CountryConfig
        from finance.models import MicroLoan
        from geodata.models import CommunityMapPoint, WMSLayer
        from livestock.models import Herd
        from logistics.models import Transporter
        from marketplace.contracts_models import BuyerContract
        from water_resources.models import WaterPoint

        for code, name, currency in [("CI", "Côte d'Ivoire", "XOF"), ("SN", "Sénégal", "XOF"), ("KE", "Kenya", "KES")]:
            CountryConfig.objects.get_or_create(code=code, defaults={"name": name, "currency": currency})

        Herd.objects.get_or_create(name="Bovins Bouaké", owner=farmer, defaults={
            "animal_type": "cattle", "count": 25, "location": Point(-5.032, 7.692, srid=4326),
        })
        WaterPoint.objects.get_or_create(name="Puits Centre Bouaké", defaults={
            "point_type": "well", "region": "Bouaké",
            "location": Point(-5.030, 7.690, srid=4326), "capacity_m3": 500,
        })
        Transporter.objects.get_or_create(name="Transport Agricole CI", defaults={
            "phone": "+2250700000099", "region": "Bouaké", "capacity_kg": 10000,
        })
        MicroLoan.objects.get_or_create(borrower=farmer, crop_type="maize", defaults={
            "amount": 150000, "purpose": "Achat semences", "status": "approved",
        })
        CommunityMapPoint.objects.get_or_create(name="Marché Bouaké", contributor=farmer, defaults={
            "category": "market", "location": Point(-5.028, 7.688, srid=4326), "verified": True,
        })
        WMSLayer.objects.get_or_create(name="FAO Soils Africa", defaults={
            "source_url": "https://www.fao.org/geoserver/wms",
            "layer_name": "fao:soils", "country": "Côte d'Ivoire",
        })
        PhytosanitaryTreatment.objects.get_or_create(crop_type="maize", week_number=3, defaults={
            "treatment_name": "Traitement préventif ravageurs",
            "product": "Bacillus thuringiensis", "dosage": "1L/ha",
        })
        BuyerContract.objects.get_or_create(buyer=admin, crop_type="maize", defaults={
            "quantity_kg": 5000, "max_price_per_kg": 300, "region": "Bouaké",
        })
        if first_parcel:
            CarbonCredit.objects.get_or_create(parcel=first_parcel, owner=farmer, defaults={
                "co2_tons_sequestered": 5.0, "period_start": date(2025, 1, 1),
                "period_end": date(2025, 12, 31),
            })

        self.stdout.write("Création données v6...")
        from agro_extensions.models import BeeHive, FishPond, SeedBankEntry
        from economy.models import InputPrice, LiveAuction
        from inclusion.models import VillageWhatsAppGroup
        from iot.v6_models import LoRaDevice, SoilStation
        from resilience.models import EarlyWarningAlert, RefugeCenter

        BeeHive.objects.get_or_create(name="Ruches Nord", owner=farmer, defaults={
            "location": Point(-5.034, 7.694, srid=4326), "honey_production_kg": 12.5,
        })
        FishPond.objects.get_or_create(name="Bassin Tilapia", owner=farmer, defaults={
            "location": Point(-5.029, 7.681, srid=4326), "stock_count": 500,
        })
        SeedBankEntry.objects.get_or_create(crop_type="maize", variety="Locale Jaune", contributor=farmer, defaults={
            "quantity_kg": 50, "region": "Bouaké", "harvest_year": 2024,
        })
        RefugeCenter.objects.get_or_create(name="École Primaire Bouaké", defaults={
            "center_type": "school", "location": Point(-5.031, 7.691, srid=4326),
            "region": "Bouaké", "capacity": 300,
        })
        EarlyWarningAlert.objects.get_or_create(title="Risque sécheresse Bouaké", defaults={
            "hazard_type": "drought", "level": "warning", "region": "Bouaké",
            "description": "Pluviométrie inférieure à la normale sur 30 jours",
        })
        VillageWhatsAppGroup.objects.get_or_create(village_name="Village Kouassi", defaults={
            "region": "Bouaké", "admin_phone": "+2250700000001", "member_count": 45,
        })
        LoRaDevice.objects.get_or_create(device_id="LORA-001", defaults={
            "name": "Capteur sol LoRa", "location": Point(-5.033, 7.693, srid=4326),
            "device_type": "soil_moisture",
        })
        SoilStation.objects.get_or_create(device_id="SOIL-001", defaults={
            "name": "Station NPK Bouaké", "location": Point(-5.032, 7.692, srid=4326),
            "ph": 5.8, "nitrogen": 45, "phosphorus": 30, "potassium": 25,
        })
        InputPrice.objects.get_or_create(product="NPK 15-15-15", region="Bouaké", defaults={
            "product_type": "fertilizer", "price_per_unit": 350, "unit": "kg",
        })
        LiveAuction.objects.get_or_create(seller=farmer, crop_type="maize", defaults={
            "quantity_kg": 200, "starting_price": 250,
            "ends_at": timezone.now() + timedelta(hours=2),
        })

        self.stdout.write("Création données v7...")
        from alerts.rule_models import AlertRule
        from cooperatives.v7_models import CooperativeVote, EquipmentReservation
        from farm_ops.models import BudgetEntry, CropSeason, FarmTask, FieldJournal, HarvestJournal, InputInventory
        from forum.poll_models import ForumPoll
        from gamification.challenge_models import SeasonalChallenge
        from incidents.ops_models import RescueVolunteer
        from training.quiz_models import Quiz, QuizQuestion

        first_parcel = Parcel.objects.filter(owner=farmer).first()
        if first_parcel:
            CropSeason.objects.get_or_create(parcel=first_parcel, year=2025, crop_type="maize", defaults={
                "planting_date": date(2025, 4, 15), "status": "active",
            })
            HarvestJournal.objects.get_or_create(
                parcel=first_parcel, owner=farmer, crop_type="maize",
                harvest_date=date(2024, 8, 20), defaults={"quantity_kg": 850, "quality_grade": "A"},
            )
            FieldJournal.objects.get_or_create(
                author=farmer, entry_date=date.today(),
                defaults={"parcel": first_parcel, "observation": "Pousse régulière, pas de ravageurs visibles.",
                          "weather_note": "Ensoleillé", "rainfall_mm": 0},
            )

        InputInventory.objects.get_or_create(owner=farmer, product_name="NPK 15-15-15", defaults={
            "product_type": "fertilizer", "quantity": 25, "unit": "kg", "alert_threshold": 30,
        })
        InputInventory.objects.get_or_create(owner=farmer, product_name="Semences maïs", defaults={
            "product_type": "seed", "quantity": 8, "unit": "kg", "alert_threshold": 10,
        })
        FarmTask.objects.get_or_create(owner=farmer, title="Traitement herbicide", defaults={
            "parcel": first_parcel, "due_date": date.today() + timedelta(days=3),
            "crop_type": "maize", "source": "calendar",
        })
        BudgetEntry.objects.get_or_create(owner=farmer, category="Vente maïs", entry_date=date(2024, 9, 1), defaults={
            "entry_type": "income", "amount": 200000, "description": "Récolte maïs",
        })
        BudgetEntry.objects.get_or_create(owner=farmer, category="Engrais", entry_date=date(2025, 4, 10), defaults={
            "entry_type": "expense", "amount": 45000,
        })
        AlertRule.objects.get_or_create(owner=farmer, name="Stock bas engrais", defaults={
            "metric": "inventory", "operator": "lt", "threshold": 30,
        })
        AlertRule.objects.get_or_create(owner=farmer, name="Humidité sol faible", defaults={
            "metric": "soil_moisture", "operator": "lt", "threshold": 30,
        })
        CooperativeVote.objects.get_or_create(cooperative=coop, title="Achat tracteur communautaire", defaults={
            "description": "Vote pour l'acquisition d'un tracteur partagé",
            "created_by": farmer, "ends_at": timezone.now() + timedelta(days=7),
        })
        EquipmentReservation.objects.get_or_create(
            cooperative=coop, equipment_name="Pulvérisateur", reserved_by=farmer,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        course = Course.objects.filter(title="Irrigation efficace").first()
        if course:
            quiz, _ = Quiz.objects.get_or_create(course=course, title="Quiz irrigation", defaults={"pass_score": 70})
            QuizQuestion.objects.get_or_create(quiz=quiz, question="Quelle est la meilleure heure pour arroser ?", defaults={
                "options": ["Midi", "Tôt le matin", "Minuit"], "correct_index": 1,
            })
        ForumPoll.objects.get_or_create(author=farmer, question="Semis maïs : avril ou mai ?", defaults={
            "options": ["Avril", "Mai", "Juin"], "votes": {"Avril": 3, "Mai": 5},
            "ends_at": timezone.now() + timedelta(days=5),
        })
        SeasonalChallenge.objects.get_or_create(title="Récolte record", defaults={
            "description": "Enregistrer 3 récoltes cette saison",
            "action": "harvest_log", "target_count": 3, "points_reward": 100,
            "region": "Bouaké", "starts_at": date.today(), "ends_at": date.today() + timedelta(days=90),
        })
        RescueVolunteer.objects.get_or_create(user=rescue, defaults={
            "skills": ["secours", "navigation"], "vehicle_type": "4x4", "region": "Abidjan",
        })

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès!"))
        self.stdout.write("Comptes: admin/admin1234, kouassi/farmer1234, secours/rescue1234")
