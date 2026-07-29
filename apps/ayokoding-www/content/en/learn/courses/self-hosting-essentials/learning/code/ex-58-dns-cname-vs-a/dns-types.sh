#!/usr/bin/env bash
# Example 58: CNAME vs A Record. (co-11)
#
# Both map a NAME to a destination, but to different KINDS of destination:
#   A     name -> IPv4 address   (a box, directly)
#   CNAME name -> another NAME   (an alias, which then resolves to an address)
# This script shows when each applies and verifies a record's TYPE. Run from
# anywhere with dig.

set -euo pipefail  # => fail fast on a bad query

# --- A record: name -> an IP (Example 13 used this) --------------------------
BOX_IP="$(cat .box-ip)"  # => the box's IPv4 (Example 1)
echo "[A]     myapp.example.com. -> ${BOX_IP}"  # => co-11: a direct name->IP mapping
dig +noall +answer myapp.example.com A  # => prints the A record (name IN A ip)

# --- CNAME: name -> another name (used to alias to a managed host) -----------
# Typical use: point a vanity domain at a PaaS / CDN hostname (Example 30's PaaS,
# or a static-site CDN) whose IP you do not control and may change.
echo "[CNAME] docs.example.com. -> myapp.hostedpaas.com."  # => an alias to ANOTHER NAME
dig +noall +answer docs.example.com CNAME 2>/dev/null || echo "         (create: docs IN CNAME myapp.hostedpaas.com)"

# --- The rule that decides (co-11) -------------------------------------------
# - Use A when you control the box's IP and it is stable (Example 13's case).
# - Use CNAME when the target is a NAME you do not control (a PaaS/CDN hostname)
#   whose underlying IP may rotate without notice.
# Caveat: a CNAME cannot coexist with other records on the SAME name, and the
# APEX (example.com, bare) traditionally could not be a CNAME (use ALIAS/ANAME
# or a flattening provider there).
# --- Verify the TYPE of an existing record -----------------------------------
TYPE_A="$(dig +short myapp.example.com A | head -1)"   # => an IP, or empty
TYPE_C="$(dig +short docs.example.com CNAME | head -1)" # => a name, or empty
echo "[verify] A -> '${TYPE_A:-<none>}' ; CNAME -> '${TYPE_C:-<none>}'"  # => co-11: record type matters