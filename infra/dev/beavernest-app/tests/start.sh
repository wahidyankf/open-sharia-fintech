#!/usr/bin/env bash
set -euo pipefail

beavernest_start=infra/dev/beavernest-app/scripts/start.sh
rg -Fq 'usage: start.sh --env-file PATH' "$beavernest_start"
rg -Fq 'scripts/preflight.sh' "$beavernest_start"
rg -Fq 'docker compose --env-file' "$beavernest_start"
! rg -q 'source .*\.env|\. .*\.env' "$beavernest_start"
