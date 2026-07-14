#!/bin/bash
# ex-04-stage-a-file: git add moves a file from the working tree into the index (co-05, co-02)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
git -c init.defaultBranch=main init -q
echo "hello" >file.txt

git add file.txt # => copies file.txt's CURRENT content into the index
#    (the staging area) -- the middle of the three-states
#    model: working tree -> index -> committed history

git status # => file.txt now lists under "Changes to be committed",
#    not "Untracked files" -- it moved out of the working
#    tree's own section entirely
