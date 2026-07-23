#!/usr/bin/env bash
# Example 36: reading a line from piped stdin
set -euo pipefail

printf 'hello from stdin\n' | { # => pipes one line of text into the command group below
  read -r line                  # => read -r reads exactly one line into $line (no backslash escaping)
  echo "got: $line"             # => echoes back exactly what was read from the pipe
}                               # => closes the command group
# => Output: got: hello from stdin
