#!/usr/bin/env bash
# Example 39: heredoc with a quoted delimiter (no expansion)
set -euo pipefail

# shellcheck disable=SC2034 # name is deliberately unused below -- that IS the point of this example
name="Ada" # => a variable that will NOT be expanded inside the heredoc below

# The quoted delimiter <<'EOF' below disables ALL expansion inside the block
# $name prints LITERALLY here, exactly as typed, because the delimiter is quoted
cat <<'EOF'
Hello, $name!
EOF
# => the bare EOF on its own line ends the heredoc
# => output: "Hello, $name!" -- the dollar sign and variable name print unexpanded
