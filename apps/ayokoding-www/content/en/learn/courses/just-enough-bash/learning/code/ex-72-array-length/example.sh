#!/usr/bin/env bash
# Example 72: array length with ${#arr[@]}
set -euo pipefail

arr=(a b c)       # => a three-element indexed array
echo "${#arr[@]}" # => # before a parameter expansion means "length of"; [@] selects every element
# => Output: 3
