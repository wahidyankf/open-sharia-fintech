#!/usr/bin/env bash
# Example 58: default values with parameter expansion
set -euo pipefail

show_name() {                # => a function that greets by name, or falls back to a default
  local name="${1:-default}" # => ${1:-default} uses $1 if set and non-empty, else the literal "default"
  echo "name: $name"         # => prints whichever value was chosen
}                            # => closes the function

show_name       # => called with NO argument, so $1 is unset and "default" is used
show_name "Ada" # => called WITH an argument, so "Ada" is used instead of the default
# => Output: "name: default" then "name: Ada"
