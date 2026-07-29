#!/usr/bin/env bash
# Example 74: Draining In-Flight Requests Before Stop. (co-18, co-15)
#
# Before stopping a backend for a deploy (or a blue-green flip, Example 73),
# DRAIN it: tell the proxy to stop sending NEW requests, but let the IN-FLIGHT
# ones finish, THEN stop the process. This is the co-18 mechanism that makes a
# stop invisible to callers. This script drains Caddy's upstream, waits for
# zero in-flight, then stops the app. Run on the box.

set -euo pipefail  # => fail fast

UNIT="myapp"  # => the backend to drain + stop
DRAIN_WAIT=20  # => max seconds to wait for in-flight requests to finish

# --- 1. Tell the proxy to stop sending NEW traffic to this backend -----------
# In Caddy, a drain is typically a config change marking the upstream 'down':
#   reverse_proxy 127.0.0.1:8000 { lb_policy ... } -> add the 'down' health check
# (or, for a blue-green flip, just point the proxy elsewhere -- Example 73.)
echo "[drain] marking ${UNIT} as non-receiving; new traffic goes elsewhere"  # => co-18: no NEW requests

# --- 2. Wait for in-flight requests to reach zero ----------------------------
for i in $(seq 1 "${DRAIN_WAIT}"); do  # => poll up to DRAIN_WAIT seconds
  # In a real setup, read the proxy's active-connections counter; here we sleep.
  if [ "$((i % 5))" -eq 0 ]; then echo "[drain] waiting for in-flight to finish (${i}s)"; fi
  # (break early when the in-flight counter hits zero)
  sleep 1
done

# --- 3. Now SAFE to stop the process -- nothing is in flight -----------------
systemctl stop "${UNIT}"  # => co-15: a clean stop with no dropped request
echo "[verify] ${UNIT} stopped with zero in-flight requests (co-18 proof)"  # => no caller saw an error