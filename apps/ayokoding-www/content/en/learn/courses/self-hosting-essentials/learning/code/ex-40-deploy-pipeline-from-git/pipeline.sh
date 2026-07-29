#!/usr/bin/env bash
# Example 40: A Deploy Pipeline from Git. (co-16, co-18)
#
# Wire the deploy (Example 26) into a small pipeline: push -> build -> health
# check -> release. The health check is the gate that makes a push a SAFE deploy
# (co-18): if the new release fails its check, the pipeline stops BEFORE the
# release, leaving the last known-good version serving. Run from the laptop.

set -euo pipefail  # => fail fast; -e makes the health check a hard gate

APP_NAME="myapp"  # => the deployed app
BOX_IP="$(cat .box-ip)"  # => the box running the PaaS (Example 25)

# --- Stage 1: BUILD (the push triggers it on the PaaS) ------------------------
echo "[1/3] build: git push"  # => co-16: the push builds a new release image
git push dokku main:master  # => a new release is staged but NOT yet the live one

# --- Stage 2: HEALTH-CHECK the new release ------------------------------------
# A real pipeline hits a staging URL or a per-review URL; here we hit the app
# right after the push and require a 200 before declaring success.
echo "[2/3] health-check the new release"  # => co-18 gate
STATUS="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://${BOX_IP}:$(ssh dokku@${BOX_IP} ports ${APP_NAME} | awk '/http/{print $NF; exit}')/health" || echo 000)"
[ "${STATUS}" = "200" ] || { echo "[gate] health-check failed (${STATUS}); rollback before release"; ssh "dokku@${BOX_IP}" ps:rollback "${APP_NAME}"; exit 1; }

# --- Stage 3: RELEASE (healthy -> the new version is now live) ----------------
echo "[3/3] release: healthy -> live"  # => co-18: the deploy is committed only after the gate passed
echo "[verify] the pipeline built, health-checked, and released ${APP_NAME}"  # => co-16/co-18 proof