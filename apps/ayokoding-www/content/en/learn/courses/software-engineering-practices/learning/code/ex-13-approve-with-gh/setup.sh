#!/bin/bash
# learning/code/ex-13-approve-with-gh/setup.sh
# ex-13: approving a PR from the terminal once the requested changes land (co-07)
# NOTE: mocked, hand-constructed transcript -- `gh` needs a real GitHub remote and network access,
# neither of which this topic's self-contained examples depend on.
set -e # => co-07: abort immediately if any command below fails

echo "test(auth): add regression test for empty-token refresh" >new_test.txt # => co-07: the requested fix from ex-12
gh pr view 142 --comments >before_approval.txt                               # => co-07: the addressed request-changes comment, for context

gh_pr_review_args=(--approve)              # => co-07: -a/--approve -- unblocks the merge
gh_pr_review_args+=(--body "LGTM")         # => co-07: -b/--body -- the reviewer's own comment text
gh pr review 142 "${gh_pr_review_args[@]}" # => co-07: reviews the SAME PR #142, now that the fix landed

gh pr view 142 --comments # => co-07: --comments -- now lists BOTH review entries,
#    request-changes followed by the approval, in order
