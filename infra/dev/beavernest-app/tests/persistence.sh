#!/usr/bin/env bash
# The only state this test owns is its mktemp directory and Compose project.
set -euo pipefail
source "$(dirname "$0")/assertions.bash"

beavernest_compose=infra/dev/beavernest-app/docker-compose.yml
grep -q '^  beavernest-app:$' "$beavernest_compose"
assert_no_match grep -Eq '^  beavernest-(be|fe):$|down -v|beavernest-be-e2e-data' "$beavernest_compose"
grep -Fq 'BEAVERNEST_BE_HOST_DATA_DIRECTORY:-/tmp/beavernest-unconfigured-data' "$beavernest_compose"
grep -Fq 'create_host_path: false' "$beavernest_compose"
