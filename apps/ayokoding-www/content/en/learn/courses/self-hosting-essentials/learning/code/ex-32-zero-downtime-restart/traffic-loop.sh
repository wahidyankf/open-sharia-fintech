#!/usr/bin/env bash
# Example 32: A Zero-Downtime Restart. (co-18)
#
# A naive "stop then start" deploy drops every in-flight request at the moment
# of the stop. This script does a HEALTH-CHECKED restart that drops no
# requests: hammer the endpoint with curl in a loop, restart the app, and prove
# the loop keeps getting 200s throughout. Run on the box in two terminals.

set -euo pipefail  # => fail fast; the traffic loop must not mask a real error

DOMAIN="myapp.example.com"  # => the public HTTPS endpoint from Example 14

# --- Run THIS in terminal 1: a continuous traffic loop that logs failures ----
echo "[traffic] curling https://${DOMAIN}/health in a loop; failures are PRINTED"  # => co-18 probe
while true; do  # => hammer until Ctrl-C
  CODE="$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "https://${DOMAIN}/health" || echo "ERR")"  # => one request
  if [ "${CODE}" != "200" ]; then echo "[drop!] $(date +%T) got ${CODE}"; fi  # => a dropped request would print here
  sleep 0.2  # => 5 requests/sec -- enough to catch a gap during the restart
done
# --- In terminal 2: restart the app, and watch terminal 1 stay clean ---------
#   systemctl restart myapp
# [verify] terminal 1 prints NO "[drop!]" lines during the restart window.
# That is co-18's zero-downtime property: the proxy + restart-on-crash + fast
# health recovery keep the endpoint answering through the cutover.