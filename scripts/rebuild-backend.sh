#!/usr/bin/env bash
# Rebuild propre du backend Docker (corrige deps manquantes type drf-spectacular).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Arrêt des conteneurs legacy sur le port 8003 (arca_gis_api)..."
docker stop arca_gis_api 2>/dev/null || true
docker rm arca_gis_api 2>/dev/null || true

echo "==> Build image backend..."
docker compose build backend

echo "==> Démarrage db + redis + backend..."
docker compose up -d db redis backend

echo "==> Attente santé Postgres..."
for i in $(seq 1 30); do
  if docker compose exec -T db pg_isready -U arca_user -d arca_gis >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "==> Migrations..."
docker compose exec -T backend python manage.py migrate --noinput

echo "==> Vérification manage.py (drf-spectacular)..."
docker compose exec -T backend python -c "import drf_spectacular; print('drf_spectacular OK')"

echo ""
echo "Backend prêt : http://localhost:8003"
echo "Tests : ./scripts/test-backend.sh"
