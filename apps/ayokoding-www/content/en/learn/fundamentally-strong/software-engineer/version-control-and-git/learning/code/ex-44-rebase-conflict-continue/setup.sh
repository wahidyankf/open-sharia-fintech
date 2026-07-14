#!/bin/bash
# ex-44-rebase-conflict-continue: resolving a rebase conflict then --continue finishes replaying commits (co-15, co-14)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com"
git -c init.defaultBranch=main init -q
echo "base" >file.txt
git add file.txt
git commit -q -m "initial"
git switch -c feature -q
echo "feature edit" >file.txt
git commit -aq -m "feature edits line"
git switch main -q
echo "main edit" >file.txt
git commit -aq -m "main edits line"
git switch feature -q

git rebase main || true # => replaying "feature edits line" onto main's new
#    tip conflicts -- both sides rewrote the same line

git status # => "You are currently rebasing" -- distinct from a
#    merge conflict's status wording, same underlying idea
echo "feature edit resolved" >file.txt # => the human resolution, replacing markers
git add file.txt                       # => marks this ONE commit's conflict as resolved
git rebase --continue                  # => resumes replaying any remaining commits after
#    the resolved one

git log --oneline --graph --all # => linear again -- the rebase, once resumed,
#    finished exactly like ex-43's conflict-free case
