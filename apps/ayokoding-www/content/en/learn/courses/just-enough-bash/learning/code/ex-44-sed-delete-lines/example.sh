#!/usr/bin/env bash
# Example 44: deleting matching lines with sed
set -euo pipefail

# queries.txt (colocated in this directory) has 4 lines; 2 contain "DROP"
sed '/DROP/d' queries.txt # => /DROP/d deletes every line that CONTAINS the pattern "DROP"
# => Output: "SELECT * FROM users;" then "INSERT INTO users VALUES (1);" -- both DROP lines are gone
