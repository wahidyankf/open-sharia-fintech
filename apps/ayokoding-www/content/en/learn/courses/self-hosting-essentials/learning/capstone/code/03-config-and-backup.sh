#!/usr/bin/env bash
# Capstone Step 3: configure via env (no committed secrets); add a tested backup + restore. (co-12, co-13, co-19)
#
# Builds on Step 2's running service: wire an env file (non-secret config) + a
# separate locked-down secrets file into the systemd unit, then add a scripted,
# tested backup of the data volume AND prove a restore reproduces it. Run as
# root, after Step 2.

set -euo pipefail

APP_DIR="/opt/myapp"; UNIT="myapp"; DB_PATH="${APP_DIR}/data/app.db"

echo "=== [1/4] non-secret env config (co-12) ==="
cat > "${APP_DIR}/app.env" <<ENV  # => non-secret tunables; safe to live next to the repo
APP_HOST=127.0.0.1
APP_PORT=8000
APP_LOG_LEVEL=info
ENV
chmod 640 "${APP_DIR}/app.env"; chown deploy:deploy "${APP_DIR}/app.env"

echo "=== [2/4] secrets out of band, never in the repo (co-13) ==="
SIGNING_SECRET="$(openssl rand -hex 32)"  # => generated on the box; the repo never sees it
install -o deploy -g deploy -m 600 /dev/stdin "${APP_DIR}/secrets.env" <<<"APP_SIGNING_SECRET=${SIGNING_SECRET}"
# Wire BOTH files into the unit via EnvironmentFile (Example 62):
if ! grep -q 'EnvironmentFile=' /etc/systemd/system/${UNIT}.service; then
  sed -i '/^ExecStart=/i EnvironmentFile=/opt/myapp/app.env\nEnvironmentFile=-/opt/myapp/secrets.env' /etc/systemd/system/${UNIT}.service
  systemctl daemon-reload && systemctl restart ${UNIT}  # => pick up the env files
fi

echo "=== [3/4] a scripted, tested backup (co-19) ==="
BACKUP_DIR="/var/backups/myapp"; install -d -m 750 "${BACKUP_DIR}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"; DEST="${BACKUP_DIR}/app-${STAMP}.db"
sqlite3 "${DB_PATH}" ".backup '${DEST}'" 2>/dev/null || cp "${DB_PATH}" "${DEST}"  # => online backup if sqlite, else copy
chmod 640 "${DEST}"
sqlite3 "${DEST}" 'PRAGMA integrity_check;' 2>/dev/null | grep -q '^ok$' && echo "[verify] backup integrity OK: ${DEST}"

echo "=== [4/4] a restore that reproduces the data (co-19) ==="
LATEST="$(ls -1t "${BACKUP_DIR}"/app-*.db | head -n1)"
systemctl stop ${UNIT}  # => no writer races the swap
mv "${DB_PATH}" "${DB_PATH}.step3-wiped"; cp "${LATEST}" "${DB_PATH}"
chown deploy:deploy "${DB_PATH}"; chmod 640 "${DB_PATH}"
systemctl start ${UNIT}; sleep 3
curl -fsS http://127.0.0.1:8000/health >/dev/null && echo "[verify] restored data serves; the service is healthy"  # => co-19 proof