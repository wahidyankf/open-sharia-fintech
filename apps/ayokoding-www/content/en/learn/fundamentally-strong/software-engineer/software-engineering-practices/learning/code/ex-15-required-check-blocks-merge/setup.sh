#!/bin/bash
# learning/code/ex-15-required-check-blocks-merge/setup.sh
# ex-15: a required status check blocks a deliberately failing commit from merging (co-09)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access.
set -e # => co-09: abort immediately if any command below fails

echo "def add(a, b): return a - b" >math.py                  # => co-09: a DELIBERATELY wrong implementation (- instead of +)
git checkout -qb fix/correct-add                             # => co-09: a branch named for the fix it CLAIMS to be
git add math.py && git commit -q -m "fix(math): correct add" # => co-09: ships the bug, disguised as a fix

gh_pr_create_args=(--title "fix(math): correct add")      # => co-09: --title -- disguises the bug as a fix
gh_pr_create_args+=(--body "Fixes the add() regression.") # => co-09: --body -- the claimed (false) fix description
gh_pr_create_args+=(--base main)                          # => co-09: --base -- targets the protected branch
gh pr create "${gh_pr_create_args[@]}"                    # => co-09: opens the PR that will hit the required check

gh pr checks 144 # => co-09: shows the required "ci / test" check's status --
#    ex-14's own "ci / test" job, now enforced by ex-15
gh pr merge 144 --squash # => co-09: attempts the merge -- expected to be BLOCKED --
#    the wrong add() fails the SAME test the required
#    check runs, so the protection rule stops it
