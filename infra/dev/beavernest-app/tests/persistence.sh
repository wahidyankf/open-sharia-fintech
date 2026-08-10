#!/usr/bin/env bash
# The only state this test owns is its mktemp directory and Compose project.
set -euo pipefail

beavernest_compose=infra/dev/beavernest-app/docker-compose.yml
rg -q '^  beavernest-app:$' "$beavernest_compose"
! rg -q '^  beavernest-(be|fe):$|down -v|beavernest-be-e2e-data' "$beavernest_compose"
rg -Fq 'BEAVERNEST_BE_HOST_DATA_DIRECTORY:-/tmp/beavernest-unconfigured-data' "$beavernest_compose"
rg -Fq 'create_host_path: false' "$beavernest_compose"
