#!/usr/bin/env bash
# capstone-solid-core: Step 4's local CI-gate runner (topic 30 co-08/co-09/co-10). Runs the
# EXACT SAME three stages ci.yml declares, in the same order, so a contributor sees the
# identical gate CI would enforce BEFORE ever opening a PR. Each stage only runs if the
# previous one exited 0 (`set -e` below is the local equivalent of ci.yml's `needs:`).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "=== STAGE 1/3: lint (ruff check + ruff format --check) ==="
.venv/bin/ruff check .
.venv/bin/ruff format --check .
echo "lint: PASS"
echo

echo "=== STAGE 2/3: test (pytest) ==="
export CAPSTONE_SOLID_CORE_DB_PATH="/tmp/ci-local-habits.db"
export CAPSTONE_SOLID_CORE_AUTH_SECRET="ci-local-not-a-real-secret"
rm -f "$CAPSTONE_SOLID_CORE_DB_PATH"
.venv/bin/python -m pytest -q
echo "test: PASS"
echo

echo "=== STAGE 3/3: build (python -m compileall app) ==="
.venv/bin/python -m compileall app
echo "build: PASS"
echo

echo "ALL STAGES GREEN"
