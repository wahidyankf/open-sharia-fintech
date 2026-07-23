#!/bin/bash
# ex-19-gitignore-basics: .gitignore patterns hide matching files from git status (co-26)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "*.log" >.gitignore # => a pattern matching any file ending in .log,
#    anywhere in the working tree
git add .gitignore
git commit -q -m "add gitignore"

touch x.log # => a NEW file that matches the ignore pattern

git status # => x.log never appears -- not as untracked, not as
#    anything -- .gitignore hid it from status entirely;
#    "nothing to commit, working tree clean" is genuinely
#    true even though x.log exists on disk right now
