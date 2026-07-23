#!/usr/bin/env bash
# Example 54: merging stderr into stdout
set -euo pipefail

noisy() {                           # => a function that writes to both stdout and stderr
  echo "info: starting"             # => an ordinary stdout line
  echo "error: something broke" >&2 # => explicitly written to stderr (fd 2), not stdout
  echo "info: done"                 # => a second ordinary stdout line
}                                   # => closes the function

noisy 2>&1 | grep error # => 2>&1 redirects stderr into stdout BEFORE the pipe, so grep sees both streams
# => Output: error: something broke -- the two "info:" lines don't match "error" and are filtered out
