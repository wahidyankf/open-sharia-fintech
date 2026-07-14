#!/usr/bin/env bash
# Example 18: Test Vs Bracket
if test -d .; then       # => `test` is the original directory-test spelling (here a shell builtin)
  echo "test: exists"    # => taken because "." (the current directory) always exists
fi                       # => Output line 1: test: exists
if [ -d . ]; then        # => [ ... ] is `test` written with bracket syntax -- the same builtin
  echo "bracket: exists" # => taken for the identical reason as above
fi                       # => Output line 2: bracket: exists
