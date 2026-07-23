#!/usr/bin/env bash
# Example 33: positional parameters -- $1, $2, $#
set -euo pipefail

set -- alpha beta gamma # => set -- simulates script arguments: $1=alpha, $2=beta, $3=gamma

echo "first: $1"  # => $1 is the first positional parameter
echo "second: $2" # => $2 is the second positional parameter
echo "count: $#"  # => $# is the total number of positional parameters (3)
# => Output: "first: alpha", "second: beta", "count: 3"
