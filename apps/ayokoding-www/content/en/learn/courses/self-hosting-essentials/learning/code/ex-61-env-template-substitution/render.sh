#!/usr/bin/env bash
# Example 61: Env-File Templating at Deploy Time. (co-12, co-21)
#
# A repo-committed TEMPLATE (app.env.tmpl) holds the SHAPE; a deploy step fills
# in the VALUES from a separate source (the box, a secret store) and writes the
# real app.env on the box -- never in the repo. This is co-12 + co-21 combined:
# reproducible config generation with no committed secret. Run on the box.

set -euo pipefail  # => fail fast; a half-rendered env file is a misconfigured app

APP_DIR="/opt/myapp"  # => the service home
ENV_FILE="${APP_DIR}/app.env"  # => the REAL file (mode 0600, gitignored); generated, not committed

# --- 1. The template ships in the repo (safe, no real values) ----------------
# app.env.tmpl looks like:
#   APP_PORT=${APP_PORT}              # placeholder filled from the environment at render time
#   APP_SIGNING_SECRET=${SECRET}      # placeholder for a secret sourced out-of-band
install -m 644 app.env.tmpl "${APP_DIR}/app.env.tmpl" 2>/dev/null || true  # => template committed; safe

# --- 2. Source the values OUT OF BAND (box env / secret file) ----------------
APP_PORT="8000"  # => a non-secret value, specific to this environment (co-12)
SECRET="$(cat "${APP_DIR}/secrets.env" | sed -n 's/^APP_SIGNING_SECRET=//p')"  # => co-13: secret read from the locked file

# --- 3. Render the real env file from the template ---------------------------
# envsubst substitutes ${VAR} from the current environment into the template.
export APP_PORT SECRET  # => make them visible to envsubst
envsubst < "${APP_DIR}/app.env.tmpl" > "${ENV_FILE}.tmp"  # => render to a temp first
chmod 600 "${ENV_FILE}.tmp" && chown deploy:deploy "${ENV_FILE}.tmp"  # => lock before it becomes real
mv -f "${ENV_FILE}.tmp" "${ENV_FILE}"  # => atomic swap; readers see old-or-new, never half
echo "[verify] rendered ${ENV_FILE} with APP_PORT + a secret, neither committed:"  # => co-12/co-21 proof
echo "         grep -c APP_ ${ENV_FILE}  # => 2 lines, and 'git log' has never seen this file"