#!/bin/bash
# ex-01-init-repository: git init creates .git/ and starts an empty repo (co-01)
set -e
WORKDIR=$(mktemp -d) && cd "$WORKDIR" # => fresh, empty scratch directory -- not a repo yet
# => (nothing under WORKDIR resembles a project yet)

git -c init.defaultBranch=main init # => creates .git/ -- this ONE call turns a plain folder
#    into a repository; -c pins the initial branch name
#    to "main" for this command only (no global config)

ls -a .git | head -5 # => .git/ genuinely exists on disk right after init
# => (HEAD, config, hooks/, objects/, refs/ all appear)

git status # => the very first status report of a brand-new repo
# => reports "No commits yet" -- there is no history at all
