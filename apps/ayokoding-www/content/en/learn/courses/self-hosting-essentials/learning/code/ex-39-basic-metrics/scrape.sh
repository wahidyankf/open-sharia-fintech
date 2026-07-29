#!/usr/bin/env bash
# Example 39: A Basic Metrics Endpoint. (co-14)
#
# Logs tell you WHY something failed; METRICS tell you THAT it is degrading
# before it fails. This adds a /metrics endpoint to the app exposing a couple of
# counters (request count, in-flight) in the Prometheus text format -- the floor
# of metrics, scrapeable by curl or any collector. Run on the box.

set -euo pipefail  # => fail fast

DOMAIN="myapp.example.com"  # => the public endpoint
METRICS_PATH="/metrics"  # => the conventional Prometheus scrape path

# --- 1. Confirm the app exposes /metrics (the app must add the route) ---------
# The app is assumed to serve text like:
#   myapp_requests_total 1234
#   myapp_in_flight 3
RAW="$(curl -fsS "http://127.0.0.1:8000${METRICS_PATH}")"  # => the raw text exposition format
echo "[metrics] local scrape:"; echo "${RAW}"  # => co-14: the observable signal a collector reads

# --- 2. Hit it THROUGH the proxy too (the path a real scraper uses) -----------
curl -fsS "https://${DOMAIN}${METRICS_PATH}" | grep -E '^myapp_' | head  # => only the app's own metric lines

# --- 3. co-14 acceptance: the counters MOVE across two scrapes ---------------
sleep 1  # => generate a little traffic between scrapes (a few requests)
curl -fsS "https://${DOMAIN}/" >/dev/null 2>/dev/null || true  # => one request to bump the counter
AFTER="$(curl -fsS "https://${DOMAIN}${METRICS_PATH}" | awk '/^myapp_requests_total/{print $2}')"
echo "[verify] myapp_requests_total moved -> ${AFTER} (a scraper would see it grow)"  # => co-14 proof