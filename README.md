# ARCA-GIS — Agro-Rescue Climate Africa

Plateforme géomatique africaine intelligente pour la gestion de l'agriculture, des urgences et du climat.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango + Channels
├── ai_module/        # FastAPI — IA climatique, NDVI, prévisions
├── mobile/           # Flutter (Android/iOS/Web PWA)
├── deploy/           # Nginx + Docker production
└── docker-compose.yml
```

## Fonctionnalités complètes

### Mobile (Flutter)
- Carte interactive OpenStreetMap avec parcelles, climat, SOS
- **Dessin de parcelles** directement sur la carte
- **Mode hors-ligne** avec cache et file SOS
- **Géofencing** — alertes à l'entrée de zones à risque
- **Suivi GPS secours** en temps réel
- **Chat incident** agriculteur ↔ secours (WebSocket)
- **Analytiques** avec graphiques (humidité, NDVI)
- **Prévisions météo** 7 jours (OpenWeatherMap / NASA)
- **Multilingue** : Français, English, Kiswahili
- **PWA** — installable depuis le navigateur
- Bouton SOS animé + analyse IA

### Backend (Django)
- API REST JWT + 10 modules
- WebSockets : alertes, GPS secours, chat
- **Météo réelle** : OpenWeatherMap + NASA POWER
- **Rapports PDF** par parcelle
- **IoT** : ingestion capteurs Arduino/Raspberry
- **Géofencing** PostGIS
- **Analytics** dashboard stats
- **Notifications push** FCM
- **Audit logs** + rate limiting
- **Dashboard admin web** : `/dashboard/`

### Module IA
- Analyse climatique (sécheresse, inondations, canicules)
- **NDVI** simulé (santé végétation)
- **Prévisions agricoles** 14 jours
- Recommandations par culture africaine

## Démarrage rapide

```bash
cp .env.example .env
docker compose up -d

# Migrations
docker run --rm --network arca-gis_default \
  -v ./backend:/app -e DATABASE_URL=postgis://arca_user:arca_secret_2024@arca_gis_postgres:5432/arca_gis \
  arca_gis_backend sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py seed_data"

# Mobile
cd mobile/arca_gis_app && flutter pub get && flutter run
```

> API : **port 8003** (8000 souvent occupé). Émulateur Android : `10.0.2.2:8003`

## Comptes démo

| Utilisateur | Mot de passe | Rôle |
|-------------|-------------|------|
| `admin` | `admin1234` | Admin |
| `kouassi` | `farmer1234` | Agriculteur |
| `secours` | `rescue1234` | Secours |

## API principale

| Endpoint | Description |
|----------|-------------|
| `POST /api/incidents/sos/` | Déclencher SOS |
| `POST /api/climate/analyze/` | Analyse IA |
| `GET /api/climate/weather/forecast/` | Prévisions 7j |
| `GET /api/core/reports/parcel/{id}/` | Rapport PDF |
| `POST /api/core/geofences/check/` | Vérifier géofencing |
| `POST /api/iot/ingest/` | Données capteur IoT |
| `GET /api/analytics/dashboard/` | Stats dashboard |
| `POST /api/notifications/register/` | Token FCM |
| `/dashboard/` | Dashboard admin web |

### WebSockets

```
ws://host:8003/ws/alerts/?token=JWT
ws://host:8003/ws/gps/?token=JWT
ws://host:8003/ws/chat/{incident_id}/?token=JWT
```

## IoT — Exemple capteur

```bash
curl -X POST http://localhost:8003/api/iot/ingest/ \
  -H "Content-Type: application/json" \
  -d '{"device_id":"IOT-BOUAKE-001","value":42.5,"unit":"%","battery":85}'
```

## Production

```bash
cd deploy && docker compose -f docker-compose.prod.yml up -d
```

Configurer : `SECRET_KEY`, `DB_PASSWORD`, `OPENWEATHER_API_KEY`, `FCM_SERVER_KEY`

## Licence

ARCA-GIS © 2024 — Open Source
