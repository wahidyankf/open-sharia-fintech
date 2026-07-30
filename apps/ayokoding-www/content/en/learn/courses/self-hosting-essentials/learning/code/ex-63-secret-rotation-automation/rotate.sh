#!/usr/bin/env bash
# Example 63: Automating Secret Rotation. (co-13, co-08)
#
# Example 21 rotated a secret BY HAND. This cron-able script automates the
# rotation on a SCHEDULE (e.g. every 90 days, ahead of cert-style expiry), with
# a SAFETY property: it writes the new secret, reloads the service, and CONFIRMS
# the reload took (rolling back the file if the service fails to come back).
# Run on the box (or schedule via Example 47's timer pattern).

set -euo pipefail  # => fail fast; a bad rotation must not leave the app broken

SECRET_PATH="/opt/myapp/secrets.env"  # => the file Example 16/21 wrote
UNIT="myapp"  # => the service to reload

# --- 1. Snapshot the current secret (rollback safety) ------------------------
BACKUP="$(mktemp)" ; cp -a "${SECRET_PATH}" "${BACKUP}"  # => keep the old value to restore on failure
trap 'rm -f "${BACKUP}"' EXIT  # => clean up the temp no matter how we exit

# --- 2. Generate + install the new secret (as in Example 21) -----------------
NEW="$(openssl rand -hex 32)"  # => fresh value, generated on the box
TMP="$(mktemp)" ; printf 'APP_SIGNING_SECRET=%s\n' "${NEW}" > "${TMP}"  # => write to temp first
chmod 600 "${TMP}" && chown deploy:deploy "${TMP}" && mv -f "${TMP}" "${SECRET_PATH}"  # => atomic install

# --- 3. Reload, then VERIFY the service came back; rollback if it did not -----
systemctl reload "${UNIT}" 2>/dev/null || systemctl restart "${UNIT}"  # => pick up the new env
sleep 3  # => give it time to bind
if ! systemctl is-active --quiet "${UNIT}"; then  # => the reload failed
  echo "[rotate] service did not come back; ROLLING BACK the previous secret"  # => co-13 safety
  mv -f "${BACKUP}" "${SECRET_PATH}" && systemctl restart "${UNIT}"  # => restore + restart on the old value
  exit 1
fi
echo "[verify] rotated secret + service healthy on the new value (co-13/co-08)"  # => rotation succeeded