#!/usr/bin/env bash
# Example 11: Install a Reverse Proxy. (co-09)
#
# The reverse proxy (Caddy here; Nginx in Example 52) terminates public traffic
# on 80/443 and forwards to the app on its local port. Caddy is chosen first
# because its config is tiny and it does automatic TLS (Example 14) by default.
# Run on the box.

set -euo pipefail  # => fail fast on a bad download or a missing keyring

# --- 1. Add Caddy's signed package repository ---------------------------------
# A vendor repo (not a random .deb) gives signed, updatable packages.
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl  # => keyring + https transport
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg  # => signed key
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' > /etc/apt/sources.list.d/caddy-stable.list  # => the repo line

# --- 2. Install Caddy (version comes from the repo; re-verify before real use) -
apt-get update  # => pick up the new repo's package list
apt-get install -y caddy  # => installs the caddy binary + a default /etc/caddy/Caddyfile

# --- 3. Confirm it serves its default welcome page on port 80 -----------------
systemctl enable --now caddy  # => start now AND on boot (the proxy must survive reboots too)
sleep 2  # => give it a moment to bind
curl -sI http://127.0.0.1:80 | head -n 1  # => co-09 proof: an HTTP status line from Caddy itself
echo "[verify] expect: HTTP/1.1 200 (or 301) -- Caddy is answering on :80"  # => the proxy is alive
echo "[next]  Example 12 points it at the app; Example 14 adds real TLS"  # => co-09 -> co-10 progression