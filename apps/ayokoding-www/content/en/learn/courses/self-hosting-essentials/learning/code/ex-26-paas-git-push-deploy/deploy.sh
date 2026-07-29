#!/usr/bin/env bash
# Example 26: Deploy via git push. (co-16)
#
# The whole point of a PaaS: ONE command (`git push`) builds and releases the
# app. Run from YOUR LAPTOP (the repo that has the app + a remote pointing at
# the PaaS). This is the contrast to Examples 7-10's hand-managed systemd unit.

set -euo pipefail  # => fail fast; a rejected push should surface, not look like success

BOX_IP="$(cat .box-ip)"  # => the box from Example 1, where the PaaS (Example 25) runs
APP_NAME="myapp"  # => the slot created by 'dokku apps:create' in Example 25

# --- 1. Add the PaaS as a git remote ------------------------------------------
# Dokku receives pushes over SSH; the remote URL is ssh://dokku@<box>/<app>.
git remote add dokku "dokku@${BOX_IP}:${APP_NAME}" 2>/dev/null || git remote set-url dokku "dokku@${BOX_IP}:${APP_NAME}"  # => idempotent

# --- 2. Push -> the PaaS builds + releases ------------------------------------
# 'main:master' maps your local main branch to Dokku's default deploy branch.
git push dokku main:master  # => co-16: the push triggers build -> release -> deploy automatically

# --- 3. Verify the push built and released a running app ---------------------
# Dokku prints a deploy URL; curl it to confirm the PaaS is serving the app.
echo "[verify] curl the deploy URL Dokku printed (default: http://${BOX_IP}:${RANDOM_PORT})"  # => co-16 proof
echo "         or: ssh dokku@${BOX_IP} ps:status ${APP_NAME}   # => shows 'running'"  # => PaaS-managed lifecycle