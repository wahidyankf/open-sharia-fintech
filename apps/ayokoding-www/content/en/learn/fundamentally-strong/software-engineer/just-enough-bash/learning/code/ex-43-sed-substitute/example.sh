#!/usr/bin/env bash
# Example 43: substituting text with sed
set -euo pipefail

# the input line contains "old" three times, once per word
echo "old cat, old hat, old mat" | sed 's/old/new/g' # => s/old/new/g substitutes EVERY "old" with "new" (g = global)
# => Output: new cat, new hat, new mat
