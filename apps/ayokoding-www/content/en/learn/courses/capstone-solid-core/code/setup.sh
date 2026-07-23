#!/usr/bin/env bash
# capstone-solid-core: one-command setup + boot (topic 05 Just Enough Bash), reused unchanged
# from the Pass-1 capstone's own setup.sh. Creates a venv, installs pinned dependencies, then
# starts the API in the foreground on http://127.0.0.1:8101 -- app/main.py's own startup call
# applies schema_v1.sql + migration_v2.sql + migration_v3.sql the first time it runs. From a
# SECOND terminal: curl http://127.0.0.1:8101/health
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"

[[ -d "$VENV_DIR" ]] || { echo "==> creating virtual environment ($VENV_DIR)" && python3 -m venv "$VENV_DIR"; }

echo "==> installing pinned dependencies"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r requirements.txt

export CAPSTONE_SOLID_CORE_AUTH_SECRET="${CAPSTONE_SOLID_CORE_AUTH_SECRET:-dev-only-not-a-real-secret-please-change}"
export CAPSTONE_SOLID_CORE_DB_PATH="${CAPSTONE_SOLID_CORE_DB_PATH:-$SCRIPT_DIR/app/habits.db}"

echo "==> starting the API on http://127.0.0.1:8101 (Ctrl-C to stop)"
exec "$VENV_DIR/bin/uvicorn" app.main:app --host 127.0.0.1 --port 8101
