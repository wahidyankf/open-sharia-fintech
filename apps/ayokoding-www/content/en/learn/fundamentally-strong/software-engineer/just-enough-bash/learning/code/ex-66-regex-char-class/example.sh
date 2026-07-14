#!/usr/bin/env bash
# Example 66: grep -E with the [[:digit:]] POSIX character class
set -euo pipefail

printf 'room42\nlobby\nfloor7\nnoexit\n' | grep -E '[[:digit:]]+'
# => [[:digit:]] is a POSIX character class, equivalent to [0-9] but portable across locales
# => + requires one or more digits somewhere in the line
# => Output: room42 then floor7 -- the two lines that contain at least one digit
