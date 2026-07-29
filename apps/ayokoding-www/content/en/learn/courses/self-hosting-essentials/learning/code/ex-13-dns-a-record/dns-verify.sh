#!/usr/bin/env bash
# Example 13: Point a DNS A Record at the Box. (co-11)
#
# An A record maps a NAME (myapp.example.com) to the box's IPv4 address, so the
# service is reachable by name and ACME (Example 14) can prove domain control.
# This script does NOT create the record (that is a one-click step at your DNS
# provider); it VERIFIES the record resolves to the box IP once it exists.

set -euo pipefail  # => fail fast; a misread IP would mislead every later check

DOMAIN="myapp.example.com"  # => the name you will request a certificate for (Example 14)
EXPECTED_IP="$(cat .box-ip)"  # => the IP Example 1 recorded -- what the record SHOULD return

# --- 1. Create the A record at your DNS provider (MANUAL, provider-specific) ---
echo "[step 1] At your DNS provider, create an A record:"
echo "         ${DOMAIN}.  IN  A  ${EXPECTED_IP}"  # => the exact record to add (name -> box IPv4)

# --- 2. Verify the record now resolves to the box IP --------------------------
# `dig +short` returns just the resolved addresses; we grep for the expected IP.
# DNS propagation can take minutes; re-run this until it matches.
RESOLVED="$(dig +short "${DOMAIN}" A | tr -d '[:space:]')"  # => the addresses the world now sees
echo "[step 2] resolved: ${RESOLVED:-<nothing-yet>}"  # => empty until propagation completes

# --- 3. co-11's acceptance check ----------------------------------------------
if [ "${RESOLVED}" = "${EXPECTED_IP}" ]; then  # => the record points where it should
  echo "[verify] PASS: ${DOMAIN} -> ${EXPECTED_IP}"  # => safe to proceed to Example 14 (TLS)
else
  echo "[verify] WAIT: not yet propagated (expected ${EXPECTED_IP}); retry in a minute"  # => co-11: poll
fi