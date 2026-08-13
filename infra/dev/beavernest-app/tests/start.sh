#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/assertions.bash"

beavernest_start=infra/dev/beavernest-app/scripts/start.sh
grep -Fq 'usage: start.sh --env-file PATH' "$beavernest_start"
grep -Fq 'scripts/preflight.sh' "$beavernest_start"
grep -Fq 'docker compose --env-file' "$beavernest_start"
assert_no_match grep -Eq 'source .*\.env|\. .*\.env' "$beavernest_start"
