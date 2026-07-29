#!/usr/bin/env bash
# Example 5: Install the App Runtime. (co-06)
#
# Before a service can run, the box needs the LANGUAGE RUNTIME it depends on.
# This pins one version (CVE-clean at authoring) so a rebuild reproduces the
# same interpreter rather than grabbing "whatever's latest." Run on the box.

set -euo pipefail  # => fail fast on a missing package or a failed download

# --- 1. Refresh the package index, then install prerequisites -----------------
apt-get update  # => fetches the latest package list (run before any apt install)
apt-get install -y curl ca-certificates  # => -y auto-confirms; curl + certs are needed by ACME later

# --- 2. Install the runtime the service needs (Python pinned) -----------------
# The service reused here is a small Python HTTP service (from backend-essentials).
# Installing python3 + venv gives a stable interpreter without a full pyenv setup.
PYTHON_VERSION="3.12"  # => pinned at authoring; re-verify CVE-clean before real use
apt-get install -y "python${PYTHON_VERSION}" "python${PYTHON_VERSION}-venv"  # => exact major.minor, reproducible

# --- 3. Create an isolated virtualenv for the app -----------------------------
# A venv keeps the app's dependencies OUT of the system Python (no version clash).
APP_DIR="/opt/myapp"  # => a single, predictable home for the service and its venv
install -d -o deploy -g deploy -m 755 "${APP_DIR}"  # => owned by the deploy user from Example 3
sudo -u deploy "python${PYTHON_VERSION}" -m venv "${APP_DIR}/venv"  # => an isolated interpreter under /opt/myapp/venv

# --- 4. Verify the pinned version is what actually got installed --------------
"${APP_DIR}/venv/bin/python" --version  # => co-06's acceptance check: prints the exact version
echo "[verify] expect: Python ${PYTHON_VERSION}.x"  # => a rebuild should print the SAME line