# ARCA-GIS — Agro-Rescue Climate Africa

Plateforme géomatique africaine intelligente pour la gestion de l'agriculture, des urgences et du climat sur une carte interactive.

## Architecture

```
ARCA-GIS/
├── backend/          # Django + GeoDjango + Channels (API REST + WebSockets)
├── ai_module/        # FastAPI — Analyse climatique & recommandations agricoles
├── mobile/           # Flutter (Android/iOS)
└── docker-compose.yml
```

### Stack technique

| Composant | Technologies |
|-----------|-------------|
| **Mobile** | Flutter, flutter_map, Provider, WebSockets |
| **Backend** | Django 5, GeoDjango, DRF, JWT, Channels, Daphne |
| **Base de données** | PostgreSQL 16 + PostGIS |
| **Temps réel** | Redis + Django Channels (WebSockets) |
| **IA** | FastAPI, scikit-learn, analyse climatique |

### Rôles utilisateurs

- **Agriculteur** — Gestion des parcelles, alertes climatiques, SOS
- **Secours** — Réception des SOS, prise en charge des incidents
- **Admin** — Gestion globale, diffusion d'alertes

## Démarrage rapide

### Prérequis

- Docker & Docker Compose
- Flutter SDK 3.12+ (pour le mobile)
- Python 3.12+ (développement local)

### 1. Lancer l'infrastructure

```bash
# Cloner et configurer
cp .env.example .env

# Démarrer PostGIS, Redis, Backend et Module IA
docker compose up -d

# Initialiser la base et les données de démo
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data
```

### 2. Lancer le backend en local (sans Docker)

```bash
cd backend
pip install -r requirements.txt

# PostgreSQL/PostGIS et Redis doivent être actifs
python manage.py migrate
python manage.py seed_data
daphne -b 0.0.0.0 -p 8000 arca_gis.asgi:application
```

### 3. Lancer le module IA

```bash
cd ai_module
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Lancer l'app mobile

```bash
cd mobile/arca_gis_app
flutter pub get
flutter run
```

> **Note Android Emulator** : L'API pointe vers `10.0.2.2:8000` (localhost de la machine hôte).
> Pour un appareil physique, modifiez `lib/config/app_config.dart` avec l'IP de votre machine.

## Comptes de démonstration

| Utilisateur | Mot de passe | Rôle |
|-------------|-------------|------|
| `admin` | `admin1234` | Administrateur |
| `kouassi` | `farmer1234` | Agriculteur |
| `secours` | `rescue1234` | Secours |

## API REST

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/auth/token/` | POST | Authentification JWT |
| `/api/users/register/` | POST | Inscription |
| `/api/users/profile/` | GET/PATCH | Profil utilisateur |
| `/api/parcels/` | GET/POST | Parcelles agricoles (GeoJSON) |
| `/api/parcels/nearby/` | GET | Parcelles à proximité |
| `/api/climate/events/` | GET | Événements climatiques |
| `/api/climate/analyze/` | POST | Analyse IA climatique |
| `/api/incidents/sos/` | POST | Déclencher un SOS |
| `/api/incidents/sos/active/` | GET | SOS actifs |
| `/api/alerts/` | GET | Liste des alertes |

### WebSocket

```
ws://localhost:8000/ws/alerts/?token=<JWT_ACCESS_TOKEN>
```

## Module IA

Le module IA (`ai_module/`) fournit :

- **Analyse climatique** — Détection sécheresse, inondations, canicules
- **Santé des cultures** — Évaluation par type de culture (maïs, riz, cacao…)
- **Recommandations** — Conseils agricoles contextualisés pour l'Afrique

```bash
# Test direct
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"lat": 7.69, "lng": -5.03, "crop_type": "maize"}'
```

## Fonctionnalités mobile

- Carte interactive (OpenStreetMap via flutter_map)
- Affichage des parcelles agricoles (polygones colorés par santé)
- Alertes climatiques en temps réel (WebSocket)
- Bouton SOS animé pour urgences
- Analyse IA avec recommandations agricoles
- Authentification JWT sécurisée
- Interface moderne Material 3

## Licence

Projet open-source — ARCA-GIS © 2026
