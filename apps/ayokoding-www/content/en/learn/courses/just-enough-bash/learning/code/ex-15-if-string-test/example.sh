#!/usr/bin/env bash
# Example 15: If String Test
a="ada"                     # => a holds the string ada
b="ada"                     # => b holds the same string, ada
if [[ "$a" == "$b" ]]; then # => [[ ]] is Bash's extended test; == compares strings for equality
  echo "equal"              # => taken because "$a" and "$b" hold identical strings
fi                          # => Output: equal
