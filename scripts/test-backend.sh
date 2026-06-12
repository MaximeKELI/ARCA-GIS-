#!/usr/bin/env bash
# Tests backend via Docker, sans recréer les conteneurs db (évite les conflits de noms).
set -euo pipefail
cd "$(dirname "$0")/.."

PYTEST_ARGS="${*:-tests/test_auth.py tests/test_parcels.py tests/test_registration.py parcels/tests.py -q}"
IMAGE="${ARCA_BACKEND_IMAGE:-arca-gis-backend}"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "==> Image $IMAGE absente, build..."
  docker compose build backend
fi

# Postgres/Redis exposés sur l'hôte (compose ou conteneurs legacy)
DB_URL="${DATABASE_URL:-postgis://arca_user:arca_secret_2024@host.docker.internal:5434/arca_gis}"
REDIS_URL="${REDIS_URL:-redis://host.docker.internal:6380/0}"

echo "==> pytest $PYTEST_ARGS"
docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  -v "$(pwd)/backend:/app" \
  -e DATABASE_URL="$DB_URL" \
  -e REDIS_URL="$REDIS_URL" \
  -e SECRET_KEY="${SECRET_KEY:-arca-gis-dev-secret-key-change-in-production}" \
  -e DEBUG=True \
  -e ALLOWED_HOSTS='*' \
  "$IMAGE" python -m pytest $PYTEST_ARGS
