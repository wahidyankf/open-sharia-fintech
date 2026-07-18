#!/bin/bash
# learning/capstone/code/pr-review.sh
# Supporting beat between Steps 2 and 3: a self-review pass, then the PR opened and reviewed
# through `gh` (co-05, co-06, co-07). NOTE: mocked, hand-constructed transcript from here on --
# `gh` needs a real GitHub remote and network access; the branch/commits it references are the
# SAME feature/points-redemption-cap branch tdd-and-history.sh actually built.
set -e # => co-06: abort immediately if any command below fails

echo "=== self-review, BEFORE opening the PR ==="  # => co-06: the author's own pass, done first
git diff --stat main feature/points-redemption-cap # => co-06: confirms the diff stays small and single-concern (2 files, 21 lines)

gh_pr_create_args=(--title "feat(loyalty): cap points redemption at 50 percent")                              # => co-07: --title -- names this PR's own concern
gh_pr_create_args+=(--body "Adds a per-transaction redemption cap. See adr-0001.md for the decision record.") # => co-07: --body -- points to the decision record
gh_pr_create_args+=(--base main)                                                                              # => co-07: --base -- the branch this PR targets
gh pr create "${gh_pr_create_args[@]}"                                                                        # => co-07: opens the PR from the terminal

gh_pr_review_args=(--comment)                                                                                                                     # => co-05: -c/--comment -- a labeled review comment, a NIT not a blocker
gh_pr_review_args+=(--body "nit: consider naming the error 'RedemptionCapExceededError' instead of a bare ValueError -- not blocking, your call") # => co-05: specific, non-blocking feedback
gh pr review 201 "${gh_pr_review_args[@]}"                                                                                                        # => co-05: reviews PR #201 opened above

echo "-- author responds: keeping the bare ValueError for this small a module, noted for later --" # => co-06: the author's own reply, in the PR thread

gh pr review 201 --approve --body "praise: the failing-test-first commit makes the intent easy to follow. LGTM" # => co-07: approval, closing the loop

gh pr view 201 --json reviewDecision # => co-07: the FINAL state -- APPROVED, ready to merge behind the CI gate (Step 3)
