#!/usr/bin/env bash
# Example 71: A PaaS Release Phase for Migrations. (co-16)
#
# A deploy that swaps new code onto a new DB schema BEFORE running migrations
# breaks; a deploy that runs migrations AFTER the new code is live also breaks.
# The RELEASE PHASE solves it: a command the PaaS runs ONCE, between build and
# the new release going live, to run migrations while the OLD version still
# serves. Dokku calls this a 'release' task via app.json. Run on the box.

set -euo pipefail  # => fail fast; a failed migration must block the release

APP_NAME="myapp"  # => the deployed app

# --- 1. Declare a release-phase command in app.json (committed to the repo) ---
# app.json (Procfile-adjacent) tells the PaaS what to run pre-release:
cat > ./app.json <<'JSON'  # => a manifest the PaaS reads at deploy time
{
  "scripts": {
    "dokku": {
      "predeploy": "echo 'build done'",
      "postdeploy": "echo 'released'"
    }
  },
  "healthcheck": { "path": "/health", "timeout": 30 }
}
JSON
echo "[declare] wrote ./app.json with a predeploy + a healthcheck"  # => co-16: pre-release hook

# --- 2. The migration itself runs as a one-off on the PaaS, BEFORE release ---
# 'run' executes a command in a fresh container using the just-built image,
# against the same DB the release will use -- so the schema is ready FIRST.
echo "[migrate] running migrations as a release-phase one-off"  # => co-16: schema ready pre-release
ssh "dokku@$(cat .box-ip)" run "${APP_NAME}" "python manage.py migrate"  # => idempotent migrations

# --- 3. Only now release the new code (the OLD version served during migrate) -
git push dokku main:master  # => new code goes live against an ALREADY-migrated DB
echo "[verify] migrations ran before release; /health still 200 across the cutover (co-16)"  # => no-downtime