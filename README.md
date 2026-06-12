# ARCA-GIS v7.6 — Agro-Rescue Climate Africa

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

## Bloc D v7.6 — IA terrain

- **Conseiller contextuel** : chat IA avec données parcelles (humidité, santé, culture)
- **Diagnostic photo** : détection maladies via `/api/ai/disease/` (caméra ou galerie)
- **Planificateur hebdomadaire** : actions IA + tâches en attente par parcelle
- **Journal vocal** : transcription → enregistrement journal de champ

| URL | Description |
|-----|-------------|
| `POST /api/ai/chat/` | Conseiller agricole (query + parcel_id optionnel) |
| `POST /api/ai/disease/` | Diagnostic maladie (image_b64 + crop_type) |
| `GET /api/ai/planner/` | Plan hebdomadaire IA + tâches |
| `POST /api/ai/voice-journal/` | Transcription vocale → journal de champ |

## Bloc C v7.5 — Stats avancées

- **Onglet Avancé** dans Analytiques : choroplèthe, Sankey budget, timeline, comparaison saisons
- **Choroplèthe carte** : humidité ou santé parcelles (toggle FAB bleu)
- **KPIs animés** : compteurs count-up sur la vue d'ensemble
- **Filtres dynamiques** : période (6/12/24 mois), métrique humidité/santé

| URL | Description |
|-----|-------------|
| `GET /api/analytics/advanced/` | Stats avancées (choroplèthe, Sankey, timeline, saisons) |
| `GET /api/analytics/advanced/?metric=health` | Choroplèthe santé parcelles |
| `GET /api/analytics/advanced/?months=24&crop=maize` | Filtres période et culture |

## Bloc B v7.4 — Agriculture complète

- **Hub agriculture étendue** : apiculture, aquaculture, semencier, agroforesterie, compost + rotation IA
- **Résilience** : refuges, alertes EWS, sécheresse 90j, simulation inondation, radio HF
- **Crédits carbone** : liste crédits + estimateur CO₂

| URL | Description |
|-----|-------------|
| `GET /api/agro/beekeeping/hives/` | Ruches |
| `GET /api/agro/aquaculture/ponds/` | Bassins piscicoles |
| `GET /api/agro/seedbank/` | Banque de semences |
| `GET /api/agro/agroforestry/plots/` | Parcelles agroforestières |
| `GET /api/agro/compost/` | Compost |
| `POST /api/agro/rotation-plan/` | Plan rotation 3 ans |
| `GET /api/resilience/refuges/` | Centres refuge |
| `GET /api/resilience/drought-ews/` | Alerte sécheresse 90j |
| `POST /api/resilience/flood-simulate/` | Simulation inondation |
| `GET /api/carbon/credits/` | Crédits carbone |
| `POST /api/carbon/estimate/` | Estimation CO₂ |

## Bloc A v7.3 — Quick wins

- **Heatmap rendements** sur la carte (toggle FAB orange)
- **Calendrier cultural visuel** (semis/récolte par culture, 4 cultures)
- **Export PDF statistiques** (`GET /api/analytics/visual/export/pdf/`)
- **Graphiques mode sombre** (cartes, axes, légendes adaptés)
- **Recherche globale** (`GET /api/core/search/?q=`) — parcelles, tâches, coop, cours, forum

## Statistiques & visualisations v7.2

- **Hub statistiques** (onglet Analytiques) : 5 onglets — Vue d'ensemble, Agriculture, Finance, Climat, Avancé
- **KPIs animés** avec sparklines, tendances % et cartes gradient
- **Courbes** : humidité sol, NDVI, pluviométrie (gradients + area fill)
- **Barres** : récoltes mensuelles, revenus vs dépenses groupés
- **Donuts** : cultures, santé parcelles, tâches, dépenses
- **Radar** : score santé fermière (5 axes)
- **Prix marché** intégrés dans l'onglet Finance

Endpoint : `GET /api/analytics/visual/`

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
| `GET /api/analytics/advanced/` | Stats avancées (Sankey, timeline, saisons) |
| `POST /api/ai/chat/` | Conseiller agricole IA contextuel |
| `POST /api/ai/disease/` | Diagnostic maladie par photo |
| `GET /api/ai/planner/` | Planificateur hebdomadaire |
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
