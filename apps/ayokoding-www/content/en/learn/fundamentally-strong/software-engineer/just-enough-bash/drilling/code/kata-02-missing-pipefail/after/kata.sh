#!/usr/bin/env bash
set -euo pipefail
# Kata 2 (FIXED): 'pipefail' makes the pipeline's exit status the FIRST
# non-zero status among all stages, so cat's real failure propagates and
# 'set -e' now correctly aborts the script instead of silently continuing.
cat /tmp/kata2-does-not-exist.txt | wc -l
echo "this line never runs -- the script already aborted above"
