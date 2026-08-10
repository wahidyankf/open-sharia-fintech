#!/usr/bin/env bash

set -euo pipefail

jq -e '.targets.dev.options.command == "scripts/start-development.sh"' apps/beavernest-be/project.json >/dev/null
jq -e '.targets.dev.options.command | contains("--host 127.0.0.1 --port 19310")' apps/beavernest-app-web/project.json >/dev/null
rg -Fq 'BEAVERNEST_BE_HTTP_LISTEN_ADDRESS=127.0.0.1' apps/beavernest-be/scripts/start-development.sh
rg -Fq 'BEAVERNEST_BE_HTTP_LISTEN_PORT=19320' apps/beavernest-be/scripts/start-development.sh
! jq -r '.scripts["beavernest:dev"]' package.json | rg -q 'docker compose|down -v'
