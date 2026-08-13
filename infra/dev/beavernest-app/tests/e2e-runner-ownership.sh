#!/usr/bin/env bash
set -euo pipefail

grep -Fq 'apps/beavernest-be-e2e/scripts/run-playwright.sh' apps/beavernest-be/scripts/run-e2e.sh
grep -Fq 'apps/beavernest-app-e2e/scripts/run-playwright.sh' apps/beavernest-be/scripts/run-e2e.sh
! grep -q 'down -v' apps/beavernest-be/scripts/run-e2e.sh
grep -Fq 'scripts/run-playwright.sh' apps/beavernest-be-e2e/project.json
grep -Fq 'scripts/run-playwright.sh' apps/beavernest-app-e2e/project.json
! grep -Eq 'docker compose|run-e2e.sh' apps/beavernest-be-e2e/scripts/run-playwright.sh apps/beavernest-app-e2e/scripts/run-playwright.sh
