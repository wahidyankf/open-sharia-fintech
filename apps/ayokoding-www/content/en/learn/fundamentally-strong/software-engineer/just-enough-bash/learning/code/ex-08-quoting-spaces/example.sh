#!/usr/bin/env bash
# Example 8: Quoting Spaces
words="a b" # => words holds a single string containing an embedded space
# shellcheck disable=SC2066 # => intentional: this loop demonstrates quoting collapsing to ONE word
for w in "$words"; do # => quoted "$words" expands to ONE word: the loop runs once
  echo "quoted: $w"   # => Output line 1: quoted: a b
done                  # => closes the quoted loop
for w in $words; do   # => unquoted $words is word-split into TWO words: the loop runs twice
  echo "unquoted: $w" # => Output line 2: unquoted: a
  # => Output line 3: unquoted: b
done # => closes the unquoted loop
