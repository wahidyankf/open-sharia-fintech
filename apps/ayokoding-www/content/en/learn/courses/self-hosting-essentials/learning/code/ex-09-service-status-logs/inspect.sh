#!/usr/bin/env bash
# Example 9: Read Service Status and Logs. (co-08, co-14)
#
# 'systemctl status' and 'journalctl -u' are the first two commands reached
# for when "is it up and why did it fail." Knowing them cold turns an outage
# into a five-minute diagnosis. Run on the box.

set -euo pipefail  # => fail fast; this script only READS, but the habit matters

UNIT="myapp"  # => the service started in Examples 7-8

# --- 1. High-level health: is it running? -------------------------------------
systemctl is-active "${UNIT}"  # => prints 'active' / 'inactive' / 'failed' (machine-parseable)
systemctl status "${UNIT}" --no-pager --full  # => human view: state, PID, recent log lines, exit code

# --- 2. The full log stream, by unit ------------------------------------------
# systemd captures the service's stdout+stderr into the journal; -u filters to ONE unit.
journalctl -u "${UNIT}" --no-pager -n 20  # => the last 20 lines for this service
journalctl -u "${UNIT}" --no-pager --since "10 min ago"  # => co-14: only recent entries

# --- 3. Watch the start/stop events live --------------------------------------
# Restart the unit and capture the lifecycle entries -- this IS co-08.
systemctl restart "${UNIT}"  # => stop + start; produces a clean pair of journal lines
journalctl -u "${UNIT}" --no-pager -n 10  # => the stop/start lines should now be visible
echo "[verify] the log should show 'Stopped' then 'Started' for ${UNIT}"  # => co-08 proof