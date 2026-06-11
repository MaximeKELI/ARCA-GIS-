# ARCA-GIS v3.0 — Agro-Rescue Climate Africa

Plateforme géomatique africaine complète pour l'agriculture, les urgences et le climat.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango (16 apps, 80+ endpoints)
├── ai_module/        # FastAPI v3 (NDVI, rendement, jumeau numérique, vocal)
├── mobile/           # Flutter v3 (Android/iOS/Web PWA)
├── deploy/           # Nginx, Docker prod, Kubernetes
└── docker-compose.yml
```

## Fonctionnalités v3.0

### Communication & Accessibilité
- **SMS/USSD SOS** — Africa's Talking / Twilio (`*384*ARCA#`)
- **Notifications vocales** — FR, EN, SW, Bambara
- **Radio communautaire** — diffusion d'alertes
- **Assistant vocal IA** — conseils multilingues
- **Paiements mobile** — Orange Money, MTN MoMo, Wave

### Agriculture avancée
- **NDVI Sentinel-2** (enhanced)
- **Détection auto parcelles** par satellite
- **Prédiction rendement** (tonnes/ha)
- **Jumeau numérique** — simulation sécheresse/inondation/optimal
- **Carte des sols** FAO/ISRIC
- **Prix marchés** en temps réel
- **Traçabilité blockchain** des récoltes

### Collaboration
- **Coopératives** — gestion collective
- **7 rôles** — agriculteur, secours, admin, agent, vétérinaire, ONG, gouvernement
- **Workflow d'approbation** des alertes
- **Drones** — missions cartographie/pulvérisation/NDVI

### Sécurité & Infrastructure
- **2FA TOTP** (Google Authenticator)
- **Signature numérique** rapports PDF
- **OpenAPI/Swagger** — `/api/docs/`
- **Rate limiting** + audit logs
- **Sentry** monitoring
- **Kubernetes** manifests
- **Multi-région** (west-africa)

### Mobile
- Mode hors-ligne, AR, chat, GPS secours, géofencing
- Coopératives, marchés, traçabilité, assistant vocal
- Multilingue FR/EN/SW, mode ultra-léger

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
| `POST /api/communications/ussd/` | Webhook USSD |
| `POST /api/communications/sms/send/` | Envoi SMS |
| `POST /api/payments/initiate/` | Paiement mobile |
| `GET /api/traceability/verify/{cert}/` | Vérifier certificat |
| `POST /api/ai/digital-twin/` | Jumeau numérique |
| `POST /api/ai/voice/` | Assistant vocal |

## Comptes démo

| User | Password | Rôle |
|------|----------|------|
| admin | admin1234 | Admin |
| kouassi | farmer1234 | Agriculteur |
| secours | rescue1234 | Secours |

## Production

```bash
cd deploy && docker compose -f docker-compose.prod.yml up -d
kubectl apply -f k8s/
```

ARCA-GIS © 2024 — Open Source
