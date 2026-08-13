#!/usr/bin/env bash
# Pure runner: CI and the lifecycle wrapper supply an already-running runtime.
set -euo pipefail

beavernest_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd -P)
cd "$beavernest_root/apps/beavernest-app-e2e"
npx bddgen
exec npx playwright test
