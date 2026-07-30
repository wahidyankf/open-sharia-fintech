#!/usr/bin/env bash
# Example 8: Enable the Service on Boot. (co-07, co-15)
#
# 'start' runs the service NOW; 'enable' makes it start on the NEXT boot too.
# Together they give the resilience property: a reboot is no longer an outage.
# Run on the box after installing /etc/systemd/system/myapp.service (Example 7).

set -euo pipefail  # => fail fast; a typo in a unit name should surface immediately

UNIT="myapp"  # => the service name (the file is /etc/systemd/system/${UNIT}.service)

# --- 1. Tell systemd a new/changed unit file exists ---------------------------
# systemd caches units; daemon-reload picks up the file written in Example 7.
systemctl daemon-reload  # => REQUIRED after any edit under /etc/systemd/system/

# --- 2. Start it now, and verify it came up -----------------------------------
systemctl start "${UNIT}"  # => launches ExecStart from the unit; Type=simple stays foreground
systemctl status "${UNIT}" --no-pager  # => co-07 proof: "active (running)" with a recent timestamp

# --- 3. Enable it so a reboot brings it back automatically --------------------
# 'enable' creates the WantedBy=multi-user.target symlink (co-15's boot hook).
systemctl enable "${UNIT}"  # => now survives a reboot; verify with Example 36's reboot test
echo "[verify] is-enabled: $(systemctl is-enabled ${UNIT})"  # => expect: enabled
echo "[next]  reboot the box (Example 36) and confirm the service returns on its own"  # => co-15 proof