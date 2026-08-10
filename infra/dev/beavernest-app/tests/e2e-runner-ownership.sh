#!/usr/bin/env bash
set -euo pipefail

rg -Fq 'apps/beavernest-be-e2e/scripts/run-playwright.sh' apps/beavernest-be/scripts/run-e2e.sh
rg -Fq 'apps/beavernest-app-web-e2e/scripts/run-playwright.sh' apps/beavernest-be/scripts/run-e2e.sh
! rg -q 'down -v' apps/beavernest-be/scripts/run-e2e.sh
rg -Fq 'scripts/run-playwright.sh' apps/beavernest-be-e2e/project.json
rg -Fq 'scripts/run-playwright.sh' apps/beavernest-app-web-e2e/project.json
! rg -q 'docker compose|run-e2e.sh' apps/beavernest-be-e2e/scripts/run-playwright.sh apps/beavernest-app-web-e2e/scripts/run-playwright.sh
