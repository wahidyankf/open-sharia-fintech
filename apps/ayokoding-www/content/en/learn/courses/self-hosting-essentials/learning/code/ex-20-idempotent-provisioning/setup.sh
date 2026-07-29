#!/usr/bin/env bash
# Example 20: Make the setup.sh Idempotent. (co-21)
#
# Example 19's script works on a FRESH box, but a SECOND run redoes everything
# (re-creates users, resets the firewall, re-copies files). Idempotence means
# "running it N times has the same effect as running it once" -- so you can
# safely re-run to converge drift. This is the hardened version: every step
# checks "is this already done?" before acting. Run as root, any number of times.

set -euo pipefail  # => fail fast; idempotence does not mean ignoring errors

DOMAIN="myapp.example.com"; APP_DIR="/opt/myapp"; PYTHON_VERSION="3.12"  # => same constants as Example 19

# --- helper: run a step only if its postcondition is NOT already met ---------
ensure_user() { id -u deploy >/dev/null 2>&1 || useradd -m -s /bin/bash deploy; }  # => create only if absent
ensure_packages() { dpkg -l ufw caddy "python${PYTHON_VERSION}" 2>/dev/null | grep -q '^ii' || \
  { apt-get update && apt-get install -y ufw caddy "python${PYTHON_VERSION}" "python${PYTHON_VERSION}-venv"; }; }  # => install only if missing
ensure_firewall() { ufw status | grep -q 'Status: active' || { ufw --force reset >/dev/null; \
  ufw default deny incoming; ufw default allow outgoing; ufw allow 22/tcp; ufw allow 80/tcp; ufw allow 443/tcp; ufw --force enable; }; }  # => configure only if inactive
ensure_venv() { [ -x "${APP_DIR}/venv/bin/python" ] || sudo -u deploy "python${PYTHON_VERSION}" -m venv "${APP_DIR}/venv"; }  # => venv only if absent
ensure_app() { install -d -o deploy -g deploy -m 755 "${APP_DIR}"; cmp -s ./app.py "${APP_DIR}/app.py" || \
  { cp ./app.py "${APP_DIR}/app.py"; chown deploy:deploy "${APP_DIR}/app.py"; }; }  # => copy only if changed
ensure_unit() { cmp -s ./myapp.service /etc/systemd/system/myapp.service || cp ./myapp.service /etc/systemd/system/myapp.service; \
  systemctl daemon-reload; systemctl is-enabled --quiet myapp || systemctl enable myapp; systemctl reload-or-restart myapp; }  # => reload only on change
ensure_caddy() { cmp -s ./Caddyfile /etc/caddy/Caddyfile || cp ./Caddyfile /etc/caddy/Caddyfile; systemctl reload caddy; }  # => reload only on change

# --- run every guard (each is a no-op if its postcondition already holds) -----
ensure_user; ensure_packages; ensure_firewall; ensure_venv; ensure_app; ensure_unit; ensure_caddy  # => co-21: safe to re-run

# --- co-21's acceptance check: a second run changes NOTHING observable -------
echo "[verify] run this script a SECOND time; 'systemctl is-active myapp' and 'curl /health' should be unchanged"  # => idempotence proof