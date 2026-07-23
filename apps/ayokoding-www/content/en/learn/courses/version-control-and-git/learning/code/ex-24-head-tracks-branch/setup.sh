#!/bin/bash
# ex-24-head-tracks-branch: HEAD and the checked-out branch resolve to the identical hash (co-04)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c hotfix -q

git rev-parse HEAD # => co-04: HEAD is a pointer to the CURRENT branch,
#    not a commit hash itself -- resolving it follows that
#    indirection down to the actual commit
git rev-parse hotfix # => resolving the branch name directly reaches the
#    SAME commit -- HEAD -> hotfix -> this one commit, and
#    both queries land on the identical hash
