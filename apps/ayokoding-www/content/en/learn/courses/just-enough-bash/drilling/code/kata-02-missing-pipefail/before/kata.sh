#!/usr/bin/env bash
set -eu
# Kata 2 (BUGGY): cat on a missing file fails, but without 'pipefail' the
# pipeline's exit status comes from the LAST command (wc -l), which still
# succeeds on empty input -- masking the real cat failure completely.
cat /tmp/kata2-does-not-exist.txt | wc -l
echo "pipeline reported success (exit 0) even though cat genuinely failed above"
