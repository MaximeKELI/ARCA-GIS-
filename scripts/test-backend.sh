#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

PYTEST_ARGS="${*:-tests/test_auth.py tests/test_parcels.py tests/test_registration.py parcels/tests.py -q}"

ensure_db() {
  if ! docker compose ps db --status running -q 2>/dev/null | grep -q .; then
    docker compose up -d db redis
    for i in $(seq 1 30); do
      if docker compose exec -T db pg_isready -U arca_user -d arca_gis >/dev/null 2>&1; then
        return
      fi
      sleep 1
    done
    echo "Postgres indisponible" >&2
    exit 1
  fi
}

ensure_db

echo "==> pytest $PYTEST_ARGS"
docker compose run --rm --no-deps \
  -e DATABASE_URL=postgis://arca_user:arca_secret_2024@db:5432/arca_gis \
  -e REDIS_URL=redis://redis:6379/0 \
  -e SECRET_KEY=arca-gis-dev-secret-key-change-in-production \
  -e DEBUG=True \
  -e ALLOWED_HOSTS='*' \
  backend python -m pytest $PYTEST_ARGS
