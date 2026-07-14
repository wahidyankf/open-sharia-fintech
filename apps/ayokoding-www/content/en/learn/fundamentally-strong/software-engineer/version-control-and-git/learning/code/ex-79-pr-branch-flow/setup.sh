#!/bin/bash
# ex-79-pr-branch-flow: a feature branch, pushed, then landed on trunk through a --no-ff "PR" merge (co-28, co-13)
set -e
ROOT=$(mktemp -d) && cd "$ROOT"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git init --bare -q remote.git # => stands in for the shared, hosted remote
#    a real pull-request review would target
mkdir work && cd work
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git remote add origin ../remote.git
git push -q origin main

git switch -c add-greeting -q # => co-28: a SHORT-LIVED branch for one
#    reviewable change, never meant to live very long
echo "hello" >greeting.txt
git add greeting.txt
git commit -q -m "add greeting file"
git push -qu origin add-greeting # => published for review, exactly what a
#    hosted pull request would be opened against

git switch main -q
git merge --no-ff add-greeting -m "Merge pull request: add greeting file" # => co-13: the "merge" button a
#    PR review UI clicks is, underneath, exactly this --
#    a --no-ff merge that preserves the branch's shape
git push -q origin main

git log --oneline --graph                  # => local trunk shows the merge commit
git -C ../remote.git log --oneline --graph # => and the shared remote's trunk
#    shows the IDENTICAL graph -- the change genuinely landed
