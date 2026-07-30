#!/usr/bin/env bash
# kata-02 (after): allow SSH FIRST, then enable (co-04, co-05).
set -euo pipefail

ufw default deny incoming   # => default-deny stance (correct)
ufw default allow outgoing  # => box can still reach out
# THE FIX: allow SSH BEFORE enabling, so the policy has a hole for your session
# the instant it goes live. Order is load-bearing: allow-then-enable, never the reverse.
ufw allow 22/tcp            # => open SSH FIRST (co-04: keep your access path open)
ufw allow 80/tcp            # => HTTP (the ACME challenge + the ->HTTPS redirect)
ufw allow 443/tcp           # => HTTPS (where the reverse proxy terminates TLS)
ufw --force enable          # => NOW enabling is safe -- port 22 is already allowed
