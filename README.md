# ARCA-GIS v6.0 — Agro-Rescue Climate Africa

Plateforme géomatique africaine complète pour l'agriculture, les urgences et le climat.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango (34 apps, 160+ endpoints)
├── ai_module/        # FastAPI v6 (LLM offline, Whisper, agent autonome, 3D twin)
├── mobile/           # Flutter v6 (offline catastrophe, enchères, pictogrammes)
├── iot/firmware/     # ESP32 + LoRaWAN
├── deploy/           # Blue/green, Grafana, Fastlane, Prometheus
├── e2e/              # Tests Playwright
└── docker-compose.yml
```

## Fonctionnalités v6.0

### Agriculture étendue (bloc 3)
- Apiculture, aquaculture, agroforesterie, semencier, compost
- Rotation culturale IA (plan 3 ans)

### Économie rurale (bloc 3)
- Enchères live WebSocket, groupes d'achat intrants
- Score crédit agricole, certificats export, prix engrais

### Résilience (bloc 3)
- Early Warning sécheresse 90j, refuges, simulation inondation
- Radio HF, mode catastrophe offline

### Inclusion (bloc 3)
- Menu pictogrammes, traduction vocale (Bambara, Wolof, Hausa)
- Groupes WhatsApp village, programme femmes rurales, nutrition

### Cartographie avancée (bloc 4)
- Timelapse satellite, profil élévation/MNT, cadastre, OpenData
- Export carte PDF

### IoT étendu (bloc 5)
- LoRaWAN, station sol NPK, pluviomètre, collier GPS bétail
- OTA firmware, Edge AI

### IA v6 (bloc 6)
- LLM local offline, Whisper, agent autonome
- Sécheresse 90j, déforestation, jumeau numérique 3D

### Production (bloc 7)
- OAuth2 Google/Microsoft, multi-tenant (`X-ARCA-Tenant`)
- Audit immuable chaîné, tests E2E Playwright
- Grafana, déploiement blue/green, Fastlane

## Démarrage

```bash
cp .env.example .env
docker compose up -d

docker exec -e DATABASE_URL=postgis://arca_user:arca_secret_2024@arca_gis_postgres:5432/arca_gis \
  arca_gis_backend sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py seed_data"

cd mobile/arca_gis_app && flutter pub get && flutter run
```

## URLs clés v6

| URL | Description |
|-----|-------------|
| `GET /api/agro/beekeeping/hives/` | Ruches |
| `GET /api/economy/auctions/` | Enchères live |
| `WS /ws/auctions/<id>/` | Enchères temps réel |
| `GET /api/resilience/refuges/` | Centres refuge |
| `GET /api/resilience/drought-ews/` | Alerte sécheresse 90j |
| `POST /api/resilience/flood-simulate/` | Simulation inondation |
| `GET /api/inclusion/pictogram-menu/` | Menu illettrés |
| `GET /api/geodata/timelapse/` | Timelapse NDVI |
| `POST /api/iot/lora/ingest/` | Données LoRaWAN |
| `POST /api/iot/ota/` | Mise à jour firmware |
| `POST /ai/llm-local` | LLM offline |
| `POST /ai/autonomous-agent` | Agent autonome |
| `GET /api/core/oauth/providers/` | OAuth2 |

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
pip install playwright pytest && pytest e2e/ -v  # nécessite backend sur :8003
```

ARCA-GIS © 2024 — Open Source
