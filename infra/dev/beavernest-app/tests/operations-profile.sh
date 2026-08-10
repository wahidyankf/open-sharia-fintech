#!/usr/bin/env bash
set -euo pipefail

beavernest_compose=infra/dev/beavernest-app/docker-compose.yml
rg -Fq 'profiles: ["operations"]' "$beavernest_compose"
rg -Fq 'command: ["backup", "--name", "${BEAVERNEST_BE_OPERATION_NAME:-operation.sqlite3}"]' "$beavernest_compose"
rg -Fq 'command: ["restore", "--name", "${BEAVERNEST_BE_OPERATION_NAME:-operation.sqlite3}"]' "$beavernest_compose"
rg -Fq 'command: ["integrity"]' "$beavernest_compose"
# beavernest-app now also bind-mounts the backup directory (matching
# preflight.sh's mandatory BEAVERNEST_BE_BACKUP_DIRECTORY validation), plus
# the two operations-profile services below.
[[ $(rg -c 'target: /var/backups/beavernest' "$beavernest_compose") -eq 3 ]]
rg -Fq 'beavernest_validate_operation_name' infra/dev/beavernest-app/scripts/operations.sh
rg -Fq 'restore refused while beavernest-app is running' infra/dev/beavernest-app/scripts/operations.sh
