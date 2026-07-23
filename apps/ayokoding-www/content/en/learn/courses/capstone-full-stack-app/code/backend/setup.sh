#!/usr/bin/env bash
# Full-stack capstone -- backend: one-command setup + boot (topic 05 Just Enough Bash pattern
# reused). Creates a venv, installs pinned dependencies, then starts the API in the foreground on
# http://127.0.0.1:8120 -- app/main.py's own startup call applies the SQLite schema (topic 10)
# the first time it runs. From a SECOND terminal: curl http://127.0.0.1:8120/health
set -euo pipefail # abort on error, on an unset var, or on a failed pipe stage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # absolute path
cd "$SCRIPT_DIR"                                           # regardless of the caller's own cwd

VENV_DIR=".venv"

[[ -d "$VENV_DIR" ]] || { echo "==> creating virtual environment ($VENV_DIR)" && python3 -m venv "$VENV_DIR"; }

echo "==> installing pinned dependencies"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r requirements.txt

# a caller MAY export these first to override them; a fresh clean-machine run gets safe defaults
export CAPSTONE2_DB_PATH="${CAPSTONE2_DB_PATH:-$SCRIPT_DIR/app/tasks.db}"
export CAPSTONE2_FRONTEND_ORIGIN="${CAPSTONE2_FRONTEND_ORIGIN:-http://127.0.0.1:8121}"

echo "==> starting the API on http://127.0.0.1:8120 (Ctrl-C to stop)"
exec "$VENV_DIR/bin/uvicorn" app.main:app --host 127.0.0.1 --port 8120 # this script IS the run command
