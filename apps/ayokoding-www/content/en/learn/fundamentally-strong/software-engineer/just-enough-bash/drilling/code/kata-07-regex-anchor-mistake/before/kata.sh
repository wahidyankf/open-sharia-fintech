#!/usr/bin/env bash
set -euo pipefail
# Kata 7 (BUGGY): meant to count lines that START WITH "ERROR", but the
# pattern has no anchor, so it also matches ERROR appearing MID-LINE
# (like the harmless "last_ERROR_count=0" debug line below). The log is
# written here so the kata is self-contained and runnable with no
# pre-existing fixture.
log="kata7-log.txt"
cat >"$log" <<'EOF'
INFO service started
ERROR disk full
DEBUG last_ERROR_count=0
INFO all clear
ERROR connection refused
EOF
matches="$(grep -c 'ERROR' "$log")"
echo "lines counted as errors: $matches"
rm -f "$log"
