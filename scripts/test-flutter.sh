#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../mobile/arca_gis_app"

flutter pub get
flutter analyze
flutter test test/
