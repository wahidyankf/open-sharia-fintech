#!/usr/bin/env bash
# Example 59: DNS TTL and Propagation Verification. (co-11)
#
# TTL (Time To Live) is how long a resolver may CACHE your record before asking
# again. A LONG TTL means fewer queries but slow changes; a SHORT TTL means fast
# changes but more DNS traffic. This script reads a record's TTL and verifies a
# change has propagated to a public resolver. Run from anywhere.

set -euo pipefail  # => fail fast

DOMAIN="myapp.example.com"  # => the record under inspection
PUBLIC_RESOLVER="1.1.1.1"  # => Cloudflare's resolver -- a "what does the world see" check

# --- 1. Read the record's configured TTL -------------------------------------
# dig +ttlid prints the TTL as the second column of the answer.
TTL="$(dig +ttlid +noall +answer @"${PUBLIC_RESOLVER}" "${DOMAIN}" A | awk '{print $2}' | head -1)"
echo "[ttl] ${DOMAIN} A has TTL ${TTL:-?}s at ${PUBLIC_RESOLVER}"  # => co-11: the cache lifetime

# --- 2. The TTL trade-off, in one sentence -----------------------------------
echo "[guide] short TTL (300s) = fast failover/changes, more queries; long TTL (86400s) = the opposite"  # => co-11

# --- 3. Propagation check: does the public resolver see the EXPECTED IP? ------
EXPECTED_IP="$(cat .box-ip 2>/dev/null || echo 192.0.2.10)"  # => what the record SHOULD return
SEEN="$(dig +short @"${PUBLIC_RESOLVER}" "${DOMAIN}" A | tr -d '[:space:]')"  # => what it actually returns
if [ "${SEEN}" = "${EXPECTED_IP}" ]; then  # => propagated
  echo "[verify] propagated at ${PUBLIC_RESOLVER}: ${DOMAIN} -> ${SEEN}"  # => co-11: change is live
else
  echo "[verify] NOT YET propagated (seen '${SEEN}', expected '${EXPECTED_IP}'); wait up to TTL=${TTL}s"  # => poll
fi