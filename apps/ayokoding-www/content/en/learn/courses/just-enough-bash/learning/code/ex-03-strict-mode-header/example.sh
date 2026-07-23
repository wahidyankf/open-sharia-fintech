#!/usr/bin/env bash
# Example 3: Strict Mode Header
set -euo pipefail # => -e exits on error, -u errors on unset vars, pipefail catches pipe failures
echo "clean run"  # => reached only because nothing above failed
# => Output: clean run
