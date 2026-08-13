#!/usr/bin/env bash
set -euo pipefail

beavernest_start=infra/dev/beavernest-app/scripts/start.sh
grep -Fq 'usage: start.sh --env-file PATH' "$beavernest_start"
grep -Fq 'scripts/preflight.sh' "$beavernest_start"
grep -Fq 'docker compose --env-file' "$beavernest_start"
! grep -Eq 'source .*\.env|\. .*\.env' "$beavernest_start"
