#!/bin/bash
# learning/code/ex-48-full-pr-review-cycle/setup.sh
# ex-48: the FULL review cycle, start to finish, entirely from the terminal (co-07, co-05, co-06)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access.
set -e # => co-07: abort immediately if any command below fails

git checkout -qb feature/loyalty-redemption                           # => co-06: a branch scoped to ONE concern
git commit --allow-empty -q -m "feat(loyalty): add points redemption" # => co-06: the feature commit this whole PR ships

gh_pr_create_args=(--title "feat(loyalty): add points redemption")                              # => co-07: step 1 -- open
gh_pr_create_args+=(--body "Adds redeem_points(). See ## Not in scope for what this excludes.") # => co-07: names what's OUT of
#    scope, same discipline as ex-49
gh_pr_create_args+=(--base main)       # => co-07: --base -- the branch this PR targets
gh pr create "${gh_pr_create_args[@]}" # => co-07: opens the PR from the terminal

gh_pr_review_args=(--request-changes)                                                                   # => co-05: step 2 -- a reviewer names a BLOCKING issue
gh_pr_review_args+=(--body "blocking: missing a test for redeeming more points than the balance holds") # => co-05: specific and actionable,
#    not a vague "looks off" comment
gh pr review 151 "${gh_pr_review_args[@]}" # => co-05: flags the SAME PR opened in step 1

echo "-- addressing the feedback --"                                                # => co-06: the fix, in a small follow-up commit
git commit --allow-empty -q -m "test(loyalty): add over-redemption regression test" # => co-06: addresses EXACTLY the
#    blocking comment above, nothing more
git push -q origin feature/loyalty-redemption # => co-07: updates the SAME open PR, not a new one

gh pr review 151 --approve --body "LGTM, thanks for adding the edge case" # => co-07: step 3 -- approve, once addressed

gh pr view 151 --comments # => co-07: the FULL cycle, in order
