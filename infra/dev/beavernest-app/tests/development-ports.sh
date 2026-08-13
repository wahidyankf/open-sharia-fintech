#!/usr/bin/env bash

set -euo pipefail

jq -e '.targets.dev.options.command == "scripts/start-development.sh"' apps/beavernest-be/project.json >/dev/null
jq -e '.name == "beavernest-app" and (.tags | index("platform:flutter") != null)' apps/beavernest-app/project.json >/dev/null
grep -Fq 'BEAVERNEST_BE_HTTP_LISTEN_ADDRESS=127.0.0.1' apps/beavernest-be/scripts/start-development.sh
grep -Fq 'BEAVERNEST_BE_HTTP_LISTEN_PORT=19320' apps/beavernest-be/scripts/start-development.sh
# `beavernest:dev` intentionally uses docker compose (matching the sibling
# `organiclever:dev` pattern) — only the destructive `down -v` reset is
# disallowed here, not `docker compose` itself.
! jq -r '.scripts["beavernest:dev"]' package.json | grep -q 'down -v'
