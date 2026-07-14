#!/usr/bin/env bash
# Example 73: ${VAR:?message} -- a required-parameter guard
set -euo pipefail

: "${INPUT:?input required}"
# => : is the no-op builtin; it still evaluates its arguments, so ${INPUT:?msg} runs even though : does nothing
# => if INPUT is unset (or empty), the script prints "input required" to stderr and exits non-zero here
# => if INPUT IS set, ${INPUT:?msg} simply expands to INPUT's value, and execution continues normally
echo "INPUT is: $INPUT" # => reached only when INPUT was actually set to a non-empty value
