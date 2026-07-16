#!/usr/bin/env bash
# Pass-1 capstone: Habit Tracker -- one-command setup + boot (topic 05 Just Enough Bash).
# Creates a venv, installs pinned dependencies, then starts the API in the foreground on
# http://127.0.0.1:8100 -- app/main.py's own startup call applies the SQLite schema (topic
# 10) the first time it runs. From a SECOND terminal: curl http://127.0.0.1:8100/health
set -euo pipefail # co-03 strict-mode: abort on error, on an unset var, or on a failed pipe stage

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" # co-07 command-substitution: absolute path
cd "$SCRIPT_DIR"                                           # regardless of the caller's own cwd (co-06 quoting: always quoted)

VENV_DIR=".venv" # co-05 variables-and-expansion

# co-10 conditionals: -d tests "directory exists"; short-circuit form keeps this a single line
[[ -d "$VENV_DIR" ]] || { echo "==> creating virtual environment ($VENV_DIR)" && python3 -m venv "$VENV_DIR"; }

echo "==> installing pinned dependencies"
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r requirements.txt

# co-05 parameter-expansion default (${v:-default}): a caller MAY export these first to
# override them; a fresh clean-machine run gets safe defaults with zero manual steps.
export CAPSTONE1_AUTH_SECRET="${CAPSTONE1_AUTH_SECRET:-dev-only-not-a-real-secret-please-change}"
export CAPSTONE1_DB_PATH="${CAPSTONE1_DB_PATH:-$SCRIPT_DIR/app/habits.db}"

echo "==> starting the API on http://127.0.0.1:8100 (Ctrl-C to stop)"
exec "$VENV_DIR/bin/uvicorn" app.main:app --host 127.0.0.1 --port 8100 # co-01: this script IS the run command
