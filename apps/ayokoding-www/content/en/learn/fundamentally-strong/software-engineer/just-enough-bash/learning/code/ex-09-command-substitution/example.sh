#!/usr/bin/env bash
# Example 9: Command Substitution
year="$(date +%Y)" # => $(...) runs `date +%Y` and captures its stdout into year
# => year now holds the current 4-digit year
echo "$year" # => Output: a 4-digit year
