#!/usr/bin/env bash
# Example 21: Rotate a Secret and Reload. (co-13, co-08)
#
# Secrets are not immortal -- a leaked or aged key must be replaceable WITHOUT
# downtime. This script generates a NEW signing secret on the box, writes it
# to the locked-down secrets file (Example 16), and gracefully reloads the
# service so the app picks up the new value. Run on the box.

set -euo pipefail  # => fail fast; a half-rotated secret (new value, old process) is a bug

SECRET_PATH="/opt/myapp/secrets.env"  # => the mode-0600, out-of-band file from Example 16
UNIT="myapp"  # => the service to reload after the swap

# --- 1. Generate a fresh secret ON THE BOX (never in the repo) ----------------
NEW_SECRET="$(openssl rand -hex 32)"  # => 256 bits; the repo never sees this value
echo "[rotate] generated a new signing secret"  # => co-13: the new value exists only in memory + the box

# --- 2. Write it to the locked-down file (atomic replace) ---------------------
# Write to a temp file then mv -> the service never reads a half-written file.
TMP="$(mktemp)"  # => a private temp path
printf 'APP_SIGNING_SECRET=%s\n' "${NEW_SECRET}" > "${TMP}"  # => the only line the file needs
chmod 600 "${TMP}" && chown deploy:deploy "${TMP}"  # => same ownership/perms as Example 16
mv -f "${TMP}" "${SECRET_PATH}"  # => atomic rename: readers see either the OLD or the NEW value, never half

# --- 3. Reload the service so the NEW secret is loaded ------------------------
# 'reload' sends SIGHUP (if the unit defines ExecReload) or falls back to restart.
systemctl reload "${UNIT}" 2>/dev/null || systemctl restart "${UNIT}"  # => co-08: lifecycle op picks up the new env
echo "[verify] the app now signs with the new secret:"  # => co-13 proof
echo "  journalctl -u ${UNIT} -n 3 --no-pager   # => a fresh 'Started'/'Reloaded' line after the swap"