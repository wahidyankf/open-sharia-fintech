#!/usr/bin/env bash
# Example 67: Alert on Health-Check Failure. (co-14)
#
# Example 18 LOGGED failures; this script ALERTS on them -- after N consecutive
# failures, not one (a single blip is noise; N in a row is an outage). Run as a
# timer (Example 47's shape) every minute; it flips to "alerting" only on a
# sustained outage. Run on the box.

set -euo pipefail  # => fail fast; a broken alert is worse than no alert

DOMAIN="myapp.example.com"  # => the public endpoint (Example 17's health probe)
THRESHOLD=3  # => consecutive failures before alerting (co-14: de-noise)
STATE_FILE="/var/lib/myapp/health.state"  # => persists the failure counter across runs

# --- 1. Read the running failure counter (persisted between ticks) ------------
install -d /var/lib/myapp ; FAILS="$(cat "${STATE_FILE}" 2>/dev/null || echo 0)"  # => last run's count

# --- 2. Probe the health endpoint --------------------------------------------
if curl -fsS --max-time 5 "https://${DOMAIN}/health" >/dev/null 2>&1; then  # => healthy
  FAILS=0  # => reset on any success (a single recovery clears the counter)
else
  FAILS=$((FAILS + 1))  # => one more consecutive failure
fi
echo "${FAILS}" > "${STATE_FILE}"  # => persist for the next tick

# --- 3. Alert only when failures cross the threshold (co-14 de-noise) --------
if [ "${FAILS}" -ge "${THRESHOLD}" ]; then  # => a SUSTAINED outage, not a blip
  echo "[ALERT] ${DOMAIN} unhealthy for ${FAILS} consecutive checks -- paging"  # => co-14: the signal
  # In real use: post to a webhook, send email, open a PagerDuty incident.
else
  echo "[ok] ${FAILS}/${THRESHOLD} consecutive failures (no alert yet)"  # => still under threshold
fi
# [verify] stop the app, wait THRESHOLD ticks, see '[ALERT]'; restart it, see the counter reset (co-14).