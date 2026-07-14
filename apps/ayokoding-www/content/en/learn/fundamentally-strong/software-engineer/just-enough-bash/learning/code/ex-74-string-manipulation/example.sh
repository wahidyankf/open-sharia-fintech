#!/usr/bin/env bash
# Example 74: ${p##*/} basename and ${f%.*} extension-stripping
set -euo pipefail # => same strict-mode header as every other example in this primer

path="/usr/local/bin/example.sh" # => a sample absolute path with several directory components
echo "${path##*/}"
# => ## deletes the LONGEST match of */ from the FRONT of path -- everything up to the last /
# => Output: example.sh

file="archive.tar.gz" # => a sample filename with a compound, two-part extension
echo "${file%.*}"
# => % deletes the SHORTEST match of .* from the BACK of file -- just the final extension
# => Output: archive.tar
