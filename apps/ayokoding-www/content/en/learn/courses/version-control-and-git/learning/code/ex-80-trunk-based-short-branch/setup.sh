#!/bin/bash
# ex-80-trunk-based-short-branch: a tiny branch, fast-forwarded straight into main, then deleted (co-28, co-12, co-11)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"

git switch -c quick-fix -q # => co-28: trunk-based development favors
#    branches this short-lived -- one commit, integrated
#    almost immediately, never accumulating drift from main
echo "fixed" >fix.txt
git add fix.txt
git commit -q -m "quick trunk fix"
git switch main -q

git merge quick-fix # => co-12: main never moved while
#    quick-fix existed, so this is a plain fast-forward --
#    no merge commit needed for such a short-lived branch
git branch -d quick-fix # => co-11: once merged, the branch
#    pointer itself has served its purpose and is deleted

git log --oneline # => main advanced to include the fix
git branch        # => quick-fix is gone -- only
#    main remains, exactly what trunk-based flow favors
