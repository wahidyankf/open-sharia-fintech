#!/usr/bin/env bash
# Example 53: a multi-stage find | grep | awk | sort pipeline
set -euo pipefail

mkdir -p logs # => builds a small real logs directory for the chore below
# auth.log gets one INFO line and one ERROR line
printf '2024-01-01 INFO auth started\n2024-01-01 ERROR auth timeout\n' >logs/auth.log
# billing.log gets one ERROR line and one INFO line
printf '2024-01-01 ERROR billing failed\n2024-01-01 INFO billing ok\n' >logs/billing.log
# extra.log gets a second ERROR line, also for the auth service
printf '2024-01-01 ERROR auth retry\n' >logs/extra.log
# => three log files simulate a real "find every service with an ERROR line" chore

find logs -name '*.log' | sort | # => finds every .log file, sorted for a deterministic file order
  xargs grep ERROR |             # => greps ERROR lines across all files; output is prefixed "path:line"
  awk '{print $3}' |             # => field 3 is the service name (field 1 is "path:date", field 2 is ERROR)
  sort -u                        # => sorts and de-duplicates the service names into a final report
# => Output: "auth" then "billing" -- two services had at least one ERROR line, alphabetically sorted
