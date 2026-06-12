#!/usr/bin/env bash
# Rebuild propre du backend Docker (corrige deps manquantes type drf-spectacular).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Arrêt du conteneur legacy arca_gis_api (port 8003)..."
docker stop arca_gis_api 2>/dev/null || true
docker rm arca_gis_api 2>/dev/null || true

echo "==> Build image backend..."
docker compose build backend

echo "==> Démarrage db + redis + backend..."
if ! docker compose up -d db redis backend 2>/dev/null; then
  echo "WARN: docker compose up a échoué (conflit db possible)."
  echo "      Utilisez Postgres sur :5434 et lancez uniquement le backend :"
  echo "      docker compose up -d backend"
fi

echo "==> Attente API (max 60s)..."
for i in $(seq 1 60); do
  if curl -sf -o /dev/null -m 2 http://127.0.0.1:8003/admin/login/ 2>/dev/null; then
    echo "API OK"
    break
  fi
  sleep 1
done

if docker compose ps backend --status running -q 2>/dev/null | grep -q .; then
  echo "==> Vérification drf-spectacular dans le conteneur..."
  docker compose exec -T backend python -c "import drf_spectacular; print('drf_spectacular OK')"
  docker compose exec -T backend python manage.py migrate --noinput
fi

echo ""
echo "Backend : http://localhost:8003"
echo "Tests   : ./scripts/test-backend.sh"
