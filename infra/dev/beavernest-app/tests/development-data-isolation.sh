#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/assertions.bash"

beavernest_development_script=apps/beavernest-be/scripts/start-development.sh
grep -Fq 'BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY' "$beavernest_development_script"
grep -Fq 'export BEAVERNEST_BE_DATA_DIRECTORY="$beavernest_canonical_directory"' "$beavernest_development_script"
grep -Fq 'unset BEAVERNEST_BE_HOST_DATA_DIRECTORY' "$beavernest_development_script"
assert_no_match grep -q 'BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY' infra/dev/beavernest-app/docker-compose.yml
