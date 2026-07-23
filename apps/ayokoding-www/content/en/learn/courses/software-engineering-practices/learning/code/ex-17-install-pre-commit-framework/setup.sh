#!/bin/bash
# learning/code/ex-17-install-pre-commit-framework/setup.sh
# ex-17: installing pre-commit and proving `git commit` now runs its configured hooks (co-10)
set -e                                                          # => co-10: abort immediately if any command below fails
WORKDIR=$(mktemp -d) && cd "$WORKDIR"                           # => co-10: fresh, throwaway scratch repo -- deterministic
export GIT_AUTHOR_NAME="Dev" GIT_AUTHOR_EMAIL="dev@example.com" # => co-10: throwaway identity -- irrelevant to whether
#    the hooks themselves pass or fail
export GIT_COMMITTER_NAME="Dev" GIT_COMMITTER_EMAIL="dev@example.com" # => co-10: throwaway identity, never the real global config
git -c init.defaultBranch=main init -q                                # => co-10: creates .git/ with branch "main", quietly

cp "$OLDPWD/.pre-commit-config.yaml" . # => co-10: this example's own config, colocated alongside it
pip install -q pre-commit              # => co-10: installs the framework itself (v4.6.0)
pre-commit install                     # => co-10: wires .git/hooks/pre-commit to call the framework

printf 'bad_var = 1   \n' >sloppy.py      # => co-10: a file with trailing whitespace -- deliberate
git add .pre-commit-config.yaml sloppy.py # => co-10: stage both files for the first commit attempt

git commit -m "chore: add pre-commit config" || true # => co-10: FIRST attempt -- expected to be BLOCKED,
#    trailing-whitespace both fails AND auto-fixes

git add sloppy.py                            # => co-10: re-stage the hook's own auto-fixed version
git commit -m "chore: add pre-commit config" # => co-10: SECOND attempt -- every hook passes now --
#    the SAME defect class ex-01's fix() commit never
#    got a chance to introduce, caught before commit
