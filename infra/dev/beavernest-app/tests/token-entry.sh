#!/usr/bin/env bash
set -euo pipefail

test -f apps/beavernest-app/lib/presentation/workspace_theme.dart
test -f apps/beavernest-app/lib/presentation/status_dashboard.dart
! rg -q 'vite|react|web-ui-token' apps/beavernest-app/lib apps/beavernest-app/web
