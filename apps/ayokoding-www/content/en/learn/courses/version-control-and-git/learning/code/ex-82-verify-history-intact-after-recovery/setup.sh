#!/bin/bash
# ex-82-verify-history-intact-after-recovery: after a reflog recovery, fsck confirms nothing is still lost (co-22)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
echo "c1" >>file.txt
git commit -aq -m "c1"
echo "c2" >>file.txt
git commit -aq -m "c2"

git reset --hard HEAD~2 -q     # => discards c1 and c2 from any branch
git reset --hard 'HEAD@{1}' -q # => and immediately recovers them via
#    reflog, exactly like ex-62

git log --graph --oneline --all # => c1 and c2 are back, reachable
#    from main again, in the normal commit graph

git fsck --lost-found # => co-22: fsck walks every object
#    Git knows about and reports anything UNREACHABLE from
#    a ref -- empty output here means every intended commit
#    is genuinely reachable, none are still dangling or lost
