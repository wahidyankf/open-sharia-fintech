#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/assertions.bash"

test -f apps/beavernest-app/lib/presentation/workspace_theme.dart
test -f apps/beavernest-app/lib/presentation/status_dashboard.dart
assert_no_match git grep -Eq -- 'vite|react|web-ui-token' -- apps/beavernest-app/lib apps/beavernest-app/web
