#!/usr/bin/env bash
# Example 36: Reboot Resilience for the Whole Stack. (co-15, co-07, co-09)
#
# The ultimate resilience test: reboot the BOX, not just the service. A correct
# stack brings the service, the proxy, and TLS back on its own -- no human, no
# pager. This script triggers a reboot and lists what to verify after. Run on
# the box. (co-15: "alive" must be the DEFAULT state, even after a reboot.)

set -euo pipefail  # => fail fast; but note this script ends by rebooting the box

DOMAIN="myapp.example.com"  # => the public HTTPS endpoint (proxy + TLS + app, all must return)
UNIT="myapp"  # => the service (Examples 7-10)

# --- 1. Pre-flight: confirm the units are ENABLED (the boot hooks) ------------
systemctl is-enabled "${UNIT}" caddy 2>/dev/null | grep -q enabled || {  # => co-07/co-15: the WantedBy symlinks exist
  echo "[abort] ${UNIT} or caddy is not 'enabled' -- it will NOT survive a reboot"; exit 1; }
echo "[pre-flight] ${UNIT} + caddy are enabled -> both return on boot"  # => the precondition for resilience

# --- 2. Reboot the box --------------------------------------------------------
echo "[reboot] scheduling; reconnect over SSH when the box answers (~60s)"  # => co-15 in action
# (Uncomment to actually reboot. Left commented so this script is safe to read.)
# shutdown -r +1 "reboot-resilience test (Example 36)"

# --- 3. After reconnect, verify the WHOLE stack returned ----------------------
cat <<'CHECK'  # => the checklist to run once SSH is back
  [post-reboot verify]
  systemctl is-active myapp caddy          # => expect: active  (co-07 self-recovery)
  curl -sI https://myapp.example.com/health # => expect: HTTP/2 200 (proxy + TLS + app, co-09/co-10)
  systemctl is-system-running              # => expect: running (not 'degraded')
CHECK
echo "[verify] if all three pass, the stack is reboot-resilient (co-15)"  # => the resilience proof