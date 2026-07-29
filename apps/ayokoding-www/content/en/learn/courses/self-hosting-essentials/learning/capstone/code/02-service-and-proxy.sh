#!/usr/bin/env bash
# Capstone Step 2: install + systemd-manage the service; put a TLS reverse proxy on a real domain. (co-06..co-10, co-15)
#
# Builds on Step 1's baseline: lay down the app + a restart-on-crash systemd
# unit, then a Caddyfile that terminates TLS on ${DOMAIN}. Verify a public HTTPS
# endpoint returns 200, AND that the service restarts after a kill (and, after a
# reboot, per Example 36's drill). Run as root, after Step 1.

set -euo pipefail

DOMAIN="myapp.example.com"; APP_DIR="/opt/myapp"; UNIT="myapp"

echo "=== [1/4] app + venv + the data volume (co-06, co-19) ==="
install -d -o deploy -g deploy -m 755 "${APP_DIR}"
[ -x "${APP_DIR}/venv/bin/python" ] || sudo -u deploy python3.12 -m venv "${APP_DIR}/venv"  # => idempotent
install -d -o deploy -g deploy -m 750 "${APP_DIR}/data"  # => the persistent volume (Example 33)
cp -n app.py "${APP_DIR}/app.py" 2>/dev/null || true; chown deploy:deploy "${APP_DIR}/app.py"  # => the service

echo "=== [2/4] the restart-on-crash systemd unit (co-07, co-15) ==="
cat > /etc/systemd/system/${UNIT}.service <<UNIT  # => write the unit in place (Example 10's policy)
[Unit]
Description=Capstone MyApp service (restart-on-crash)
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
User=deploy
WorkingDirectory=/opt/myapp
Environment=APP_DB_PATH=/opt/myapp/data/app.db
ExecStart=/opt/myapp/venv/bin/python /opt/myapp/app.py
Restart=always
RestartSec=3
StartLimitIntervalSec=60
StartLimitBurst=5
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload && systemctl enable --now ${UNIT}  # => start now + on boot (co-15)

echo "=== [3/4] the TLS reverse proxy on a real domain (co-09, co-10) ==="
cat > /etc/caddy/Caddyfile <<CADDY  # => Caddy auto-obtains the cert via ACME (Example 14)
${DOMAIN} {
  reverse_proxy 127.0.0.1:8000
  header {
    Strict-Transport-Security "max-age=31536000; includeSubDomains"
    X-Content-Type-Options "nosniff"
  }
}
CADDY
systemctl reload caddy  # => triggers ACME on first request; serves HTTPS

echo "=== [4/4] verify: public HTTPS 200 + restart-on-crash ==="
sleep 3
STATUS="$(curl -s -o /dev/null -w '%{http_code}' "https://${DOMAIN}/health" || echo 000)"  # => full public path
[ "${STATUS}" = "200" ] && echo "[verify] https://${DOMAIN}/health -> 200" || { echo "[verify] FAIL: ${STATUS}"; exit 1; }
PID="$(systemctl show -p MainPID --value ${UNIT})"; kill -9 "${PID}" 2>/dev/null || true  # => simulate a crash
sleep 4; systemctl is-active --quiet ${UNIT} && echo "[verify] service restarted itself after a kill"  # => co-15 proof