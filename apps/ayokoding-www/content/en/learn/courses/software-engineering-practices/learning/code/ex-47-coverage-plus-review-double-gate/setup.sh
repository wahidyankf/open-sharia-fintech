#!/bin/bash
# learning/code/ex-47-coverage-plus-review-double-gate/setup.sh
# ex-47: coverage passes but an UNREVIEWED risky diff is still blocked by the second gate (co-12, co-05, co-09)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access.
set -e # => co-09: abort immediately if any command below fails

gh_pr_create_args=(--title "refactor(payments): switch to async settlement")    # => co-05: --title -- names the genuinely RISKY refactor
gh_pr_create_args+=(--body "Reworks payment settlement to run asynchronously.") # => co-05: async settlement touches money -- exactly
#    the kind of change a coverage number can't judge
gh_pr_create_args+=(--base main)       # => co-05: --base -- the branch this refactor targets
gh pr create "${gh_pr_create_args[@]}" # => co-05: opens the PR from the terminal

gh pr checks 150 # => co-12: shows coverage-baseline's own status --
#    passing here does NOT mean this PR is safe to merge
gh pr view 150 --json reviewDecision # => co-05: shows the review status independently --
#    still unreviewed, regardless of the coverage result
gh pr merge 150 --squash # => co-09: attempts the merge -- expected to be BLOCKED --
#    coverage alone was never sufficient by design
