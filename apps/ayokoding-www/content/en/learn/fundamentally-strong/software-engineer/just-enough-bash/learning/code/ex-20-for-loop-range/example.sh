#!/usr/bin/env bash
# Example 20: For Loop Range
for i in {1..5}; do # => {1..5} is brace expansion: it expands to 1 2 3 4 5 before the loop runs
  echo -n "$i "     # => -n suppresses echo's trailing newline, keeping output on one line
done                # => Output: 1 2 3 4 5 (trailing space, no final newline yet)
echo                # => prints one final newline so the shell prompt starts cleanly
