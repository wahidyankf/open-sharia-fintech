#!/bin/sh
# Example 82: a POSIX-portable script -- identical output under sh and bash
# Only POSIX sh constructs are used here: [ ] instead of [[ ]], no arrays, no <<<,
# and $(( )) arithmetic expansion instead of the (( )) command form -- $(( )) IS
# POSIX-legal on its own; only the (( )) compound-command syntax is bash-only.

count=0 # => a plain scalar variable; POSIX sh has no array data type at all
for word in one two three; do
  # => a plain word-list for-loop, fully POSIX-legal (no C-style for, which IS bash-only)
  count=$((count + 1)) # => $(( )) arithmetic expansion works the same in POSIX sh and bash
  if [ "$word" = "two" ]; then
    # => [ ] is the POSIX test command; [[ ]] is a bash-only keyword, deliberately avoided here
    echo "found: $word" # => Output (when word is "two"): found: two
  fi                    # => closes the if
done                    # => closes the for-loop

echo "count: $count" # => Output: count: 3, identical whether this file runs under sh or bash
