#!/usr/bin/env bash
set -euo pipefail

beavernest_development_script=apps/beavernest-be/scripts/start-development.sh
rg -Fq 'BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY' "$beavernest_development_script"
rg -Fq 'export BEAVERNEST_BE_DATA_DIRECTORY="$beavernest_canonical_directory"' "$beavernest_development_script"
rg -Fq 'unset BEAVERNEST_BE_HOST_DATA_DIRECTORY' "$beavernest_development_script"
! rg -q 'BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY' infra/dev/beavernest-app/docker-compose.yml
