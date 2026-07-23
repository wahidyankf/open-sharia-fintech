#!/usr/bin/env bash
# Example 49: translating characters with tr
set -euo pipefail

# a lowercase greeting to be uppercased
echo "hello world" | tr 'a-z' 'A-Z' # => tr maps each char in set 1 (a-z) to the char at the same position in set 2 (A-Z)
# => Output: HELLO WORLD
