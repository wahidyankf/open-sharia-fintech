#!/usr/bin/env bash
# Example 29: PaaS Env Config and Secrets. (co-12, co-16)
#
# On a PaaS, config and secrets are set via the PaaS CLI (stored in the PaaS,
# injected into the container at runtime) -- NOT in the repo. This is co-12/co-13
# applied to the PaaS altitude: the same "config in env, never in code" rule,
# with the PaaS as the env provider. Run on the box (or via the dokku remote).

set -euo pipefail  # => fail fast; a typo'd key name silently misconfigures the app

APP_NAME="myapp"  # => the app deployed in Example 26

# --- 1. Set NON-SECRET config (safe to read, like Example 15's app.env) -------
dokku config:set "${APP_NAME}" APP_LOG_LEVEL=info APP_FEATURE_NEW_CACHE=false  # => co-12: tunables, via PaaS

# --- 2. Set a SECRET (generated here, stored ONLY in the PaaS, never in git) --
SIGNING_SECRET="$(openssl rand -hex 32)"  # => generated in this shell; the repo never sees it
dokku config:set "${APP_NAME}" "APP_SIGNING_SECRET=${SIGNING_SECRET}"  # => co-13: secret lives in the PaaS, not the repo

# --- 3. Confirm the app sees the values at runtime ----------------------------
# 'config:show' lists the keys (Dokku redacts nothing here, so keep this box private);
# a restart makes the new env take effect for the running container.
dokku ps:restart "${APP_NAME}"  # => rebuild the env into the running process
echo "[verify] the running app now reads these env vars:"  # => co-12/co-13 proof
echo "  ssh dokku@<box> config:show ${APP_NAME}   # => APP_* keys are present"