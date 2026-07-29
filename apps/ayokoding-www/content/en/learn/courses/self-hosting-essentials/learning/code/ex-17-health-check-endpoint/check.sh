#!/usr/bin/env bash
# Example 17: A Health-Check Endpoint Through the Proxy. (co-14)
#
# A health endpoint (/health) is the floor of observability: a 200 means "the
# app is up and answering"; anything else means trouble. This script adds a
# /health route to the app and curls it THROUGH the proxy (the full public
# path), so the check exercises proxy + app together. Run on the box.

set -euo pipefail  # => fail fast; a monitoring script must surface, not swallow, errors

DOMAIN="myapp.example.com"  # => the TLS-terminated domain from Example 14
HEALTH_PATH="/health"  # => the conventional probe path (Example 6's app already answers "ok" here)

# --- 1. Confirm the app answers /health directly (loopback) -------------------
# Isolate the app from the proxy first: if THIS fails, the proxy is not the bug.
curl -fsS "http://127.0.0.1:8000${HEALTH_PATH}" >/dev/null  # => -f fails on non-2xx; isolates the app

# --- 2. Now hit it THROUGH the proxy (the full public path) -------------------
# This is the real health check a monitor (Example 18) will run: HTTPS + proxy + app.
STATUS="$(curl -s -o /dev/null -w '%{http_code}' "https://${DOMAIN}${HEALTH_PATH}")"  # => just the status code
echo "[health] ${DOMAIN}${HEALTH_PATH} -> HTTP ${STATUS}"  # => co-14: the observable liveness signal

# --- 3. co-14's acceptance check: a clean 200 ---------------------------------
if [ "${STATUS}" = "200" ]; then  # => the whole path (TLS, proxy, app) is healthy
  echo "[verify] PASS: healthy (200)"  # => safe for Example 18's monitor to rely on
else
  echo "[verify] FAIL: unhealthy (${STATUS})"  # => co-14: a non-200 is the alert condition
  exit 1
fi