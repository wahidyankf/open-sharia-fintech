#!/bin/bash
# learning/code/ex-18-pre-commit-run-all-files/setup.sh
# ex-18: `pre-commit run --all-files` checks every tracked file, not only what changed (co-10)
set -e                                                          # => co-10: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-10: fresh, throwaway scratch repo -- deterministic
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-10: throwaway identity -- irrelevant to whether
#    the hooks themselves pass or fail
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-10: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-10: creates .git/ with branch "main", quietly
cp "$OLDPWD/.pre-commit-config.yaml" .                                # => co-10: this example's own config, colocated alongside it

printf 'def a():\n    return 1\n' >module_a.py         # => co-10: an OLD file, already clean, committed long ago
printf 'def b():\n    return 2\n' >module_b.py         # => co-10: a SECOND old file, also already clean
git add . && git commit -m "chore: initial modules" -q # => co-10: both files enter history BEFORE ex-17 existed --
#    hooks were never run against them at commit time

pip install -q pre-commit # => co-10: installs the framework itself (v4.6.0)

pre-commit run --all-files # => co-10: the point of THIS example -- scoped to the
#    whole tracked tree, not `git diff`'s changed set
