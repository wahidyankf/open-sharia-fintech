#!/usr/bin/env bash
# Example 42: counting matches with grep -c
set -euo pipefail

# sample.log (colocated in this directory) has 4 lines, 2 of which contain "error"
grep -c error sample.log # => -c prints only the COUNT of matching lines, not the lines themselves
# => Output: 2
