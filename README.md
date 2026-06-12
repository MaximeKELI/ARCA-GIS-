# ARCA-GIS v7.2 — Agro-Rescue Climate Africa

Plateforme géomatique africaine complète pour l'agriculture, les urgences et le climat.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango (35 apps, 180+ endpoints)
├── ai_module/        # FastAPI v6 (LLM offline, Whisper, agent autonome, 3D twin)
├── mobile/           # Flutter v7 (carnet récolte, sync offline, votes coop)
├── iot/firmware/     # ESP32 + LoRaWAN
├── deploy/           # Blue/green, Grafana, Fastlane, Prometheus
├── e2e/              # Tests Playwright
└── docker-compose.yml
```

## Fonctionnalités v7.0 — Opérations autonomes

### Gestion fermière (100 % interne)
- Carnet de récolte, journal de champ, stock intrants
- Planificateur de tâches (génération depuis calendrier cultural)
- Budget fermier, calculateur de prêt, comparateur parcelles

### Alertes & sync
- Règles d'alertes personnalisables (humidité, stock, tâches)
- Sync offline bidirectionnelle (SOS, récoltes, journal, tâches)
- Simulateur USSD intégré (sans opérateur externe)

### Coopérative & formation
- Votes coopératifs, réservation équipement
- Quiz formation avec certificats PDF téléchargeables
- Dashboard par rôle (agriculteur, secours, admin)

### Cartographie & traçabilité
- Import/export GeoJSON, mesure distance/surface
- QR parcelle, historique modifications

### v6 inclus
- Apiculture, aquaculture, enchères live, EWS sécheresse 90j
- LLM offline, agent autonome, OAuth2, multi-tenant, E2E Playwright

## Démarrage

```bash
cp .env.example .env
docker compose up -d

docker exec -e DATABASE_URL=postgis://arca_user:arca_secret_2024@arca_gis_postgres:5432/arca_gis \
  arca_gis_backend sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py seed_data"

cd mobile/arca_gis_app && flutter pub get && flutter run
```

## URLs clés v7

| URL | Description |
|-----|-------------|
| `GET /api/farm/harvests/` | Carnet de récolte |
| `GET /api/farm/harvests/stats/` | Statistiques récolte |
| `GET /api/farm/tasks/` | Tâches agricoles |
| `POST /api/farm/tasks/generate/` | Générer tâches calendrier |
| `GET /api/farm/inventory/` | Stock intrants |
| `GET /api/farm/budget/summary/` | Budget fermier |
| `GET /api/alerts/rules/` | Règles d'alertes |
| `POST /api/alerts/rules/evaluate/` | Évaluer règles |
| `GET /api/cooperatives/votes/` | Votes coop |
| `GET /api/training/quizzes/<id>/` | Quiz formation |
| `GET /api/training/certificates/<id>/download/` | Certificat PDF |
| `GET /api/analytics/visual/` | Statistiques visuelles (KPIs, courbes, radar) |
| `GET /api/analytics/heatmap/` | Heatmap rendements |
| `POST /api/core/offline/sync/` | Queue sync offline |
| `POST /api/communications/ussd/simulate/` | Simulateur USSD |
| `GET /api/core/activity/` | Fil d'activité |
| `GET /api/core/bookmarks/` | Favoris |
| `GET /api/parcels/export/csv/` | Export CSV parcelles |
| `GET /api/parcels/<id>/history/` | Historique modifications |
| `GET /api/cooperatives/<id>/members/` | Annuaire membres |
| `GET /api/parcels/<id>/qr/` | QR parcelle |

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
