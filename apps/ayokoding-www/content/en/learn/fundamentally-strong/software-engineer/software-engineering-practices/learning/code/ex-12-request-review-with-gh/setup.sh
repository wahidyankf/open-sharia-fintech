#!/bin/bash
# learning/code/ex-12-request-review-with-gh/setup.sh
# ex-12: requesting changes on an open PR from the terminal (co-07)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access,
# neither of which this topic's self-contained examples depend on.
set -e # => co-07: abort immediately if any command below fails

gh_pr_review_args=(--request-changes)                                                  # => co-07: -r/--request-changes -- blocks merge
gh_pr_review_args+=(--body "needs a regression test for the empty-token refresh path") # => co-07: -b/--body -- the reviewer's own comment text
gh pr review 142 "${gh_pr_review_args[@]}"                                             # => co-07: reviews PR #142 (opened in Example 9)

gh pr view 142 --comments # => co-07: --comments -- lists every review/comment,
#    the request-changes entry included, in order
