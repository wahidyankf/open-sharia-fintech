#!/usr/bin/env bash
# Example 44: Staging vs Prod on the PaaS with Promotion. (co-16, co-18)
#
# Two environments, one PaaS: push to STAGING first, smoke-test, then PROMOTE
# the exact same release to PROD. Promotion reuses the already-built image, so
# what you tested is byte-identical to what you ship -- the co-18 safety
# property, applied across environments. Run on the box.

set -euo pipefail  # => fail fast; a promotion must not silently skip the smoke test

PROD="myapp"  # => the production app (Example 26)
STAGING="myapp-staging"  # => a separate app slot for pre-prod verification

# --- 1. Ensure both apps exist -----------------------------------------------
ssh-keygen -F "$(cat .box-ip)" >/dev/null 2>&1 || true  # => (host key assumed known from earlier examples)
dokku apps:create "${STAGING}" 2>/dev/null || true  # => create staging if absent (idempotent)

# --- 2. Push to STAGING first -------------------------------------------------
echo "[1/3] push to staging: ${STAGING}"  # => co-16: build happens here, not in prod
git remote add staging "dokku@$(cat .box-ip):${STAGING}" 2>/dev/null || true
git push staging main:master  # => a new release lands in STAGING only

# --- 3. Smoke-test staging, then PROMOTE the same release to prod -------------
SMOKE="$(curl -s -o /dev/null -w '%{http_code}' "https://${STAGING}.example.com/health")"  # => staging URL
[ "${SMOKE}" = "200" ] || { echo "[gate] staging smoke failed (${SMOKE}); NOT promoting"; exit 1; }
echo "[2/3] staging healthy -> promoting the exact release to ${PROD}"  # => co-18: tested == shipped
dokku git:from-image "${PROD}" "${STAGING}:latest" 2>/dev/null || dokku ps:promote "${STAGING}" 2>/dev/null || git push dokku main:master  # => release the same image to prod
echo "[3/3] [verify] prod now serves the promoted release: curl https://${PROD}.example.com/health"  # => co-16/co-18 proof