#!/bin/bash
# learning/code/ex-09-pr-create-with-gh/setup.sh
# ex-09: opening a pull request end to end from the terminal with `gh pr create` (co-07)
# NOTE: mocked, hand-constructed transcript (DD-20/DD-30 self-contained-example rule) -- `gh` needs a
# real GitHub remote and network access, neither of which this topic's examples depend on.
set -e # => co-07: abort immediately if any command below fails

git checkout -qb feature/auth-token-refresh                    # => co-07: the branch this PR is opened FROM
git commit --allow-empty -m "feat(auth): add token refresh" -q # => co-07: the branch's own commit (co-02 grammar)
git push -q origin feature/auth-token-refresh                  # => co-07: publishes the branch -- a PR needs a remote ref

gh_pr_create_args=(--title "feat(auth): add token refresh")                                                                  # => co-07: --title/-t -- mirrors the lead commit's subject
gh_pr_create_args+=(--body "Adds Client.refresh_token() so a session survives access-token expiry without a full re-login.") # => co-07: --body/-b
gh_pr_create_args+=(--base main)                                                                                             # => co-07: --base -- the branch this PR targets
gh pr create "${gh_pr_create_args[@]}"                                                                                       # => co-07: opens the PR without leaving the terminal

gh pr view --json number,title,baseRefName,url # => co-07: --json selects exactly the fields this
#    example verifies against, nothing extra
