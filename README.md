# ARCA-GIS v5.0 — Agro-Rescue Climate Africa

Plateforme géomatique africaine complète pour l'agriculture, les urgences et le climat.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango (30 apps, 130+ endpoints)
├── ai_module/        # FastAPI v5 (RAG, prix ML, rendement fusion, drone)
├── mobile/           # Flutter v5 (mentorat, abonnements, dark mode, élevage)
├── iot/firmware/     # ESP32 capteurs sol
├── deploy/           # Nginx, Docker prod, K8s, Prometheus
└── docker-compose.yml
```

## Fonctionnalités v5.0

### Intégrations réelles
- **OpenWeatherMap** + NASA POWER (fallback météo)
- **NASA FIRMS** — détection feux de brousse
- **FCM push** — notifications mobiles
- **WhatsApp Business** — alertes via Twilio
- **Backup S3** — sauvegarde automatique (boto3)
- **Factures PDF** — génération ReportLab

### Nouveaux modules métier
- **Élevage** — troupeaux, alertes vétérinaires
- **Gestion de l'eau** — puits, barrages, quotas, conflits
- **Micro-crédit** — prêts agricoles saisonniers
- **Logistique** — transporteurs, devis expédition
- **Cartographie participative** — points communautaires OSM
- **Couches WMS** — données géographiques externes
- **Multi-pays** — CI, SN, ML, KE configurables
- **Crédits carbone** — estimation CO₂ par parcelle
- **Contrats B2B** — acheteurs exportateurs
- **Prévision prix** — ML marchés agricoles
- **Calendrier phytosanitaire** — traitements par semaine
- **Météo communautaire** — rapports agriculteurs
- **Dispatch secours** — assignation agent le plus proche
- **Checklists évacuation** — inondation, sécheresse, feu
- **Heatmap rendement** — visualisation régionale

### IA v5
- **Agent RAG** — conseils agronomiques conversationnels
- **Prévision prix** — tendances marchés
- **Rendement fusion** — NDVI + météo + sol
- **Optimisation intrants** — engrais, semences
- **Analyse drone** — ravageurs par zone
- **Estimation carbone** — crédits par culture

### Mobile v5
- Écrans **mentorat**, **abonnements**, **élevage**
- **Mode sombre**
- **Tuiles offline** téléchargeables
- **App KaiOS** (`web/kaios.html`)
- **EXIF géoloc** — position depuis photo

### Infrastructure
- **Portail développeurs** — `/developers/`
- **Prometheus** — monitoring
- **Tests v5** — pytest étendu
- **CI/CD** — GitHub Actions

### Héritage v1-v4
SMS/USSD, 2FA, NDVI, jumeau numérique, blockchain, drones, forum, gamification, assurance, GDPR, etc.

## Démarrage

```bash
cp .env.example .env
docker compose up -d

docker exec -e DATABASE_URL=postgis://arca_user:arca_secret_2024@arca_gis_postgres:5432/arca_gis \
  arca_gis_backend sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py seed_data"

cd mobile/arca_gis_app && flutter pub get && flutter run
```

## URLs clés

| URL | Description |
|-----|-------------|
| `http://localhost:8003/api/docs/` | Swagger OpenAPI |
| `http://localhost:8003/developers/` | Portail développeurs |
| `GET /api/livestock/herds/` | Troupeaux |
| `GET /api/water/points/` | Points d'eau |
| `POST /api/finance/loans/` | Micro-crédit |
| `GET /api/logistics/transporters/` | Transporteurs |
| `POST /api/carbon/estimate/` | Crédits carbone |
| `GET /api/climate/wildfires/` | Feux NASA FIRMS |
| `POST /api/communications/whatsapp/send/` | WhatsApp |
| `POST /api/notifications/send/` | Push FCM |
| `GET /api/marketplace/price-forecast/` | Prévision prix |
| `GET /api/analytics/heatmap/` | Heatmap rendement |
| `POST /api/incidents/<id>/dispatch/` | Dispatch secours |

## Comptes démo

| User | Password | Rôle |
|------|----------|------|
| admin | admin1234 | Admin |
| kouassi | farmer1234 | Agriculteur |
| secours | rescue1234 | Secours |

## Tests

```bash
cd backend && pytest tests/ -v
cd mobile/arca_gis_app && flutter analyze
```

ARCA-GIS © 2024 — Open Source
