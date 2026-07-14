#!/usr/bin/env bash
# Example 38: heredoc with variable expansion
set -euo pipefail

name="Ada" # => a variable to interpolate inside the heredoc body

# This example proves an unquoted heredoc behaves like a double-quoted string: variables expand
# The unquoted delimiter <<EOF below means variables ARE expanded inside the block
# $name is substituted with its value BEFORE cat ever receives the text
cat <<EOF
Hello, $name!
Welcome.
EOF
# => the bare EOF on its own line ends the heredoc
# => output: "Hello, Ada!" followed by "Welcome." -- $name was expanded to "Ada"
