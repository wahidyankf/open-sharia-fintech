#!/usr/bin/env bash
# Example 72: Scaling a Process Type. (co-16)
#
# A PaaS lets you scale each process type (Example 70) to N instances
# INDEPENDENTLY -- web to 3 for more HTTP capacity, worker to 1 if jobs are
# light. The PaaS load-balances across the instances and restarts any that die.
# This is the fleet-management shape a managed platform absorbs for you (the
# contrast to the single self-hosted process in Examples 7-10). Run on the box.

set -euo pipefail  # => fail fast; a failed scale must not look like success

APP_NAME="myapp"  # => the deployed app (Example 70's two-type Procfile)

# --- 1. Scale the WEB process type to 3 instances ----------------------------
dokku ps:scale "${APP_NAME}" web=3  # => co-16: three web instances behind the PaaS proxy
echo "[scale] web=3 (the PaaS load-balances inbound HTTP across them)"  # => capacity up

# --- 2. Scale the WORKER process type to 1 (jobs are light) ------------------
dokku ps:scale "${APP_NAME}" worker=1  # => co-16: one worker; bump this when the queue backs up
echo "[scale] worker=1 (scale up if the queue depth grows)"  # => independent of web

# --- 3. Verify both types are running at the requested counts ----------------
echo "[report] current process counts for ${APP_NAME}:"  # => co-16 proof
dokku ps:report "${APP_NAME}" | grep -E 'Processes|web|worker' || dokku ps:list "${APP_NAME}" 2>/dev/null || true
echo "[verify] web x3, worker x1 -- each supervised + restarted on failure by the PaaS"  # => co-16 payoff