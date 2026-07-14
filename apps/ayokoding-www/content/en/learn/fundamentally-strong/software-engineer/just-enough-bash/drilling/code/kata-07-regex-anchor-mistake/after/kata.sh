#!/usr/bin/env bash
set -euo pipefail
# Kata 7 (FIXED): the ^ anchor (via grep -E, though -E is not even
# required for a plain ^ anchor -- kept for consistency with this
# primer's other -E examples) restricts matches to lines that actually
# START WITH "ERROR", excluding ERROR appearing mid-line. The log is
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
matches="$(grep -Ec '^ERROR' "$log")"
echo "lines counted as errors: $matches"
rm -f "$log"
