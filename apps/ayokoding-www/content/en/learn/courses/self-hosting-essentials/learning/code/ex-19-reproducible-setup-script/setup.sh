#!/usr/bin/env bash
# Example 19: A Reproducible setup.sh. (co-21)
#
# Capture the WHOLE box setup from Examples 1-16 as one script, so a clean
# machine converges to the SAME baseline unattended. This is co-21's core
# move: "the box's setup is captured as scripts so it can be rebuilt, not
# remembered." Run as root on a fresh box (or in a local VM).

set -euo pipefail  # => fail fast; a half-applied setup is worse than a clean failure

DOMAIN="myapp.example.com"  # => the domain DNS (Example 13) will point here
APP_DIR="/opt/myapp"  # => the service home used across every prior example
PYTHON_VERSION="3.12"  # => pinned runtime (Example 5)

echo "=== [1/5] system packages + runtime ==="  # => co-21: every step is numbered and echoed
apt-get update && apt-get install -y curl ca-certificates ufw python${PYTHON_VERSION} python${PYTHON_VERSION}-venv  # => Ex 4 + 5 fused

echo "=== [2/5] deploy user + firewall ==="  # => Ex 3 + 4
id -u deploy >/dev/null 2>&1 || useradd -m -s /bin/bash deploy  # => create user only if absent (idempotent-ish; Ex 20 hardens)
ufw --force reset >/dev/null  # => start from a clean firewall slate
ufw default deny incoming && ufw default allow outgoing  # => co-05 default-deny stance
ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp  # => the only open ports
ufw --force enable  # => policies LIVE

echo "=== [3/5] app + venv ==="  # => Ex 5 + 6
install -d -o deploy -g deploy -m 755 "${APP_DIR}"  # => service home, owned by deploy
sudo -u deploy "python${PYTHON_VERSION}" -m venv "${APP_DIR}/venv"  # => isolated interpreter
cp ./app.py "${APP_DIR}/app.py" && chown deploy:deploy "${APP_DIR}/app.py"  # => the service code (from Ex 6)

echo "=== [4/5] systemd unit + enable ==="  # => Ex 7 + 8
cp ./myapp.service /etc/systemd/system/myapp.service  # => the restart-on-crash unit from Example 10
systemctl daemon-reload && systemctl enable --now myapp  # => start now + on boot (co-15)

echo "=== [5/5] reverse proxy + TLS ==="  # => Ex 11 + 14
apt-get install -y caddy  # => (repo add omitted for brevity; see Example 11 in full)
cp ./Caddyfile /etc/caddy/Caddyfile  # => the TLS config from Example 14, using ${DOMAIN}
systemctl reload caddy  # => obtain the cert + serve HTTPS

echo "=== DONE: a healthy HTTPS endpoint should now answer ==="  # => co-21: one script -> whole box
curl -fsS "https://${DOMAIN}/health" && echo " [verify] 200 OK"  # => the end-to-end acceptance check