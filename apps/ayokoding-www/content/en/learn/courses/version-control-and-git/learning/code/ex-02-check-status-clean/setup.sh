#!/bin/bash
# ex-02-check-status-clean: a fresh repo names its branch and reports nothing to commit (co-05)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR"
git -c init.defaultBranch=main init -q # => -q suppresses the "Initialized empty..." banner --
#    only the deliberate `git status` output matters here

git status # => "On branch main" names the current branch by name
# => "nothing to commit" -- true even with zero commits,
#    because there are also zero untracked/modified files
