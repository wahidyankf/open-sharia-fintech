#!/usr/bin/env bash
# Example 31: function-local variables with `local`
set -euo pipefail

name="global" # => an outer variable named name, holding "global"

set_name() {              # => defines a function that tries to change name
  local name="local-only" # => local creates a NEW name, scoped only to this function call
  echo "inside: $name"    # => reads the function-local name, not the outer one
}                         # => closes the function; the local name is destroyed here

set_name              # => calls set_name; its local name never touches the outer one
echo "outside: $name" # => the outer name is completely unchanged
# => Output: "inside: local-only", then "outside: global"
