#!/usr/bin/env bash
# Example 23: Break Continue
for i in 1 2 3 4 5 6; do  # => iterates the literal numbers 1 through 6
  if ((i == 5)); then     # => arithmetic test: true only when i equals 5
    break                 # => exits the loop immediately, skipping 5 and 6 entirely
  fi                      # => closes the break-triggering if
  if ((i % 2 == 0)); then # => arithmetic test: true for even i
    continue              # => skips the rest of this iteration's body, jumping to the next i
  fi                      # => closes the continue-triggering if
  echo "$i"               # => only reached for odd i values that are less than 5
  # => Output: 1, then 3 (2/4 skipped by continue, loop stops before 5)
done # => closes the for loop
