#!/usr/bin/env bash
# Example 42: Disaster Rebuild from Script and Backup. (co-21, co-19)
#
# The ultimate test of reproducibility: PRETEND the box is gone, stand up a
# BRAND-NEW box from Example 20's setup.sh + Example 34's backup, and confirm
# the service returns with its data. This is the drill that proves co-21 ("can
# be rebuilt, not remembered") and co-19 (the backup actually restores). Run as
# root on a FRESH box.

set -euo pipefail  # => fail fast; a rebuild that silently skips a step is not a rebuild

DOMAIN="myapp.example.com"  # => the domain DNS must point at THIS new box first (Example 13)
BACKUP_DIR="/var/backups/myapp"  # => where the latest backup from the OLD box now lives (copied over)

# --- 1. Re-provision the box from the idempotent setup script (co-21) ---------
echo "[1/3] running setup.sh to converge the new box to the known baseline"  # => Example 20
./setup.sh  # => installs runtime, user, firewall, service, proxy, TLS -- unattended

# --- 2. Restore the data from the backup carried over from the old box --------
echo "[2/3] restoring data from the latest backup"  # => co-19
LATEST="$(ls -1t "${BACKUP_DIR}"/app-*.db | head -n1)"  # => newest backup
install -d -o deploy -g deploy -m 750 /opt/myapp/data  # => the volume dir (Example 33)
cp "${LATEST}" /opt/myapp/data/app.db && chown deploy:deploy /opt/myapp/data/app.db && chmod 640 /opt/myapp/data/app.db  # => restore
systemctl restart myapp  # => pick up the restored DB

# --- 3. Verify the service is back, with its data, over HTTPS (co-21 proof) ---
echo "[3/3] end-to-end verify"  # => the whole point
curl -fsS "https://${DOMAIN}/health" >/dev/null && echo "[verify] healthy on the rebuilt box"  # => co-21
echo "[verify] data restored: curl https://${DOMAIN}/items (the rows written before the loss)"  # => co-19