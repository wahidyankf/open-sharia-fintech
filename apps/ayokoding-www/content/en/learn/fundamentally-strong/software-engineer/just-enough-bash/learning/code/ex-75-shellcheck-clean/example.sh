#!/usr/bin/env bash
# Example 75: a correct script that shellcheck reports zero findings for
set -euo pipefail # => same strict-mode header as every other example in this primer

name="world"           # => a normal, safely-assigned local variable
echo "Hello, ${name}!" # => a properly double-quoted expansion; nothing here trips any shellcheck rule
# => shellcheck example.sh (below) reports zero findings for exactly this reason: nothing here is unsafe
