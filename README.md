# ARCA-GIS v4.0 — Agro-Rescue Climate Africa

Plateforme géomatique africaine complète pour l'agriculture, les urgences et le climat.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango (23 apps, 100+ endpoints)
├── ai_module/        # FastAPI v4 (diagnostic photo, irrigation, ML persisté)
├── mobile/           # Flutter v4 (forum, formation, gamification, diagnostic)
├── iot/firmware/     # ESP32 capteurs sol
├── deploy/           # Nginx, Docker prod, Kubernetes
└── docker-compose.yml
```

## Fonctionnalités v4.0

### Nouveautés principales
- **Abonnements freemium** — plans gratuit, agriculteur, coopérative
- **Forum communautaire** — échanges par région
- **Formation vidéo** — cours agricoles avec progression
- **Gamification** — badges, points, classement
- **Assurance paramétrique** — polices sécheresse/inondation
- **API partenaires** — clés `X-ARCA-API-Key` pour ONG/gouvernement
- **Mentorat** — sessions agriculteur expérimenté / débutant
- **Marketplace B2B** — annonces de vente de récoltes
- **Calendrier cultural** — semis/récoltes par région
- **Diagnostic maladies** — analyse photo IA
- **Irrigation intelligente** — conseils basés humidité sol
- **IoT étendu** — bouées fluviales, pièges à insectes
- **Appels vocaux SOS** — Twilio Voice
- **GDPR** — export/suppression données personnelles
- **Dashboard ONG** — stats régionales + export CSV
- **Tuiles offline** — cache cartographique Flutter
- **Mode feature phone** — interface ultra-légère
- **CI/CD** — GitHub Actions (backend, IA, Flutter)
- **Backup S3** — sauvegarde planifiée

### Héritage v1-v3
SMS/USSD, 2FA, NDVI Sentinel, jumeau numérique, blockchain, drones, paiements mobile, chat, GPS secours, géofencing, coopératives, OpenAPI/Swagger.

## Démarrage

```bash
cp .env.example .env
docker compose up -d

# Migrations
docker run --rm --network arca-gis_default -v ./backend:/app \
  -e DATABASE_URL=postgis://arca_user:arca_secret_2024@arca_gis_postgres:5432/arca_gis \
  arca_gis_backend sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py seed_data"

# Mobile
cd mobile/arca_gis_app && flutter pub get && flutter run
```

## URLs clés

| URL | Description |
|-----|-------------|
| `http://localhost:8003/api/docs/` | Swagger OpenAPI |
| `http://localhost:8003/dashboard/` | Dashboard admin |
| `GET /api/analytics/ngo/stats/` | Stats ONG/gouvernement |
| `GET /api/analytics/ngo/export/?format=csv` | Export parcelles CSV |
| `POST /api/communications/voice/call/` | Appel vocal SOS |
| `GET /api/marketplace/listings/` | Annonces B2B |
| `GET /api/climate/calendar/` | Calendrier cultural |
| `POST /api/climate/irrigation/advice/` | Conseil irrigation |
| `GET /api/gamification/leaderboard/` | Classement |
| `GET /api/core/gdpr/export/` | Export données RGPD |
| `POST /api/iot/buoys/ingest/` | Données bouée fluviale |
| `POST /api/iot/pest-traps/ingest/` | Données piège insectes |

## Comptes démo

| User | Password | Rôle |
|------|----------|------|
| admin | admin1234 | Admin |
| kouassi | farmer1234 | Agriculteur |
| secours | rescue1234 | Secours |

## Tests & CI

```bash
cd backend && pytest tests/ -v
cd mobile/arca_gis_app && flutter analyze
```

## Production

```bash
cd deploy && docker compose -f docker-compose.prod.yml up -d
kubectl apply -f k8s/
```

ARCA-GIS © 2024 — Open Source
