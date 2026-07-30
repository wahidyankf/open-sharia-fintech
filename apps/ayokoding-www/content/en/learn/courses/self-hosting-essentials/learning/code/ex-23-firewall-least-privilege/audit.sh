#!/usr/bin/env bash
# Example 23: Firewall Least-Privilege Audit. (co-05, co-04)
#
# Example 4 opened {22, 80, 443} and denied the rest. But services bind ports
# over time, and "what's listening" drifts from "what's allowed." This audit
# reconciles the two: list every LISTENING port, then tighten ufw so the
# allowed set is EXACTLY the required set. Run on the box.

set -euo pipefail  # => fail fast; a security audit must not paper over a finding

# --- 1. What is ACTUALLY listening? -------------------------------------------
echo "[listening] sockets bound on this box:"  # => the ground truth a firewall must match
ss -tulnp | grep LISTEN || true  # => -t TCP -u UDP -l listening -n numeric -p process (needs root)

# --- 2. What does ufw currently ALLOW? ----------------------------------------
echo "[ufw] currently allowed:"  # => the policy; should be a SUBSET of "listening + needed"
ufw status  # => co-05: every line here is a deliberately-open door

# --- 3. Tighten: remove any rule for a port NOT in the required set -----------
REQUIRED="22 80 443"  # => the only ports this stack needs (SSH, HTTP, HTTPS)
echo "[audit] any allowed port NOT in {${REQUIRED}} is drift to remove:"  # => co-04: least privilege
# (In a real run, delete stray rules with: ufw delete allow <port>/<proto>)
echo "         e.g. 'ufw delete allow 8080/tcp' for a port nothing should use"  # => remediation shape

# --- 4. co-05 acceptance: the allowed set == the required set -----------------
ALLOWED="$(ufw status | awk '/ALLOW/ {print $1}' | grep -oE '^[0-9]+' | sort -u | tr '\n' ' ')"
echo "[verify] allowed = '${ALLOWED}' (expected: '${REQUIRED} ')"  # => a clean match = least privilege achieved