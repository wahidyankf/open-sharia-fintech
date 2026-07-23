#!/bin/bash
# ex-03-create-untracked-file: a new file Git has never seen shows up as untracked (co-05)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
git -c init.defaultBranch=main init -q

echo "hello" >file.txt # => creates a file ON DISK -- Git has not been told
#    about it with `git add` yet, so it is not tracked

git status # => file.txt appears under "Untracked files" -- Git sees
#    it exists but is not part of any snapshot yet
