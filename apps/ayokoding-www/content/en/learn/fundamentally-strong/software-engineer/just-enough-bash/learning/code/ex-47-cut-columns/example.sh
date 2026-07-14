#!/usr/bin/env bash
# Example 47: extracting a CSV column with cut
set -euo pipefail

# people.csv (colocated in this directory) has a header row plus two data rows
cut -d, -f2 people.csv # => -d, sets the delimiter to a comma; -f2 keeps only the 2nd field
# => Output: "age" (the header), then "30", then "25"
