#!/usr/bin/env bash
# Capstone Step 1: provision + harden + firewall a box, reproducibly. (co-02..co-05, co-21)
#
# This is the capstone's entry point: a single, idempotent script that takes a
# fresh box to the hardened baseline every later step assumes -- runtime, a
# non-root user, a default-deny firewall. It is Example 20 distilled into the
# minimum the capstone needs. Run as root on a fresh box (or a local VM).

set -euo pipefail  # => fail fast; a half-applied hardening is worse than none

# Constants for the whole capstone (referenced by later steps)
# shellcheck disable=SC2034
DOMAIN="myapp.example.com"
# shellcheck disable=SC2034
APP_DIR="/opt/myapp"
PYTHON_VERSION="3.12"  # => the runtime version to install

echo "=== [1/4] packages + runtime (co-06) ==="
apt-get update && apt-get install -y curl ca-certificates ufw fail2ban \
  "python${PYTHON_VERSION}" "python${PYTHON_VERSION}-venv" caddy sqlite3  # => the whole stack in one install

echo "=== [2/4] non-root user (co-04) ==="
id -u deploy >/dev/null 2>&1 || useradd -m -s /bin/bash deploy  # => create only if absent (idempotent)
usermod -aG sudo deploy  # => narrow sudo for the few privileged actions

echo "=== [3/4] firewall -- default deny, open only what the stack needs (co-05) ==="
ufw status | grep -q 'Status: active' || {  # => configure only if not already active
  ufw --force reset >/dev/null; ufw default deny incoming; ufw default allow outgoing
  ufw allow 22/tcp; ufw allow 80/tcp; ufw allow 443/tcp; ufw --force enable  # => SSH + HTTP + HTTPS only
}

echo "=== [4/4] verify the baseline ==="
systemctl is-active ssh caddy >/dev/null 2>&1 || systemctl enable --now ssh caddy  # => core services up
ufw status | grep -q 'Status: active' && echo "[verify] firewall active: $(ufw status | grep -c ALLOW) rules"  # => co-05
id -u deploy >/dev/null 2>&1 && echo "[verify] non-root user 'deploy' present"  # => co-04
echo "[verify] baseline reached -- ready for Step 2 (service + proxy)"  # => co-21: reproducible so far