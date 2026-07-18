---
title: "Artifact: PR Description Scoped to One Concern"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 51
---

> ex-11 &middot; exercises co-06 &middot; a pull-request description a reviewer can summarize in one
> sentence.

A description scoped to one concern states what changed, why, and how it was checked -- and nothing
else. A reviewer reading it should be able to restate the PR's purpose in a single sentence before
ever opening the diff.

```text
## What

Adds `Client.refresh_token(old: str) -> str`, so an expiring session token can be renewed without a
full re-login.

## Why

Support tickets show ~4% of daily active sessions hit a hard logout mid-checkout when the access
token expires -- refreshing in place removes that failure mode entirely.

## How this was checked

- Added `test_refresh_token_returns_new_token` and `test_refresh_token_rejects_expired_refresh_token`
  (both pass locally: `pytest -k refresh_token`).
- Manually verified against the staging auth service: a token refreshed 30 seconds before expiry
  keeps the session alive with no re-login prompt.

## Not in scope

Refresh-token rotation policy (tracked separately: TECH-DEBT-041) is intentionally out of scope --
this PR only adds the refresh call itself.
```

**Verify**: a reviewer can restate this PR's purpose in one sentence ("lets an expiring session
token refresh in place instead of forcing a re-login") after reading only the `## What`/`## Why`
sections -- satisfying co-06's single-concern rule. The `## Not in scope` section actively prevents
scope creep by naming the adjacent work it deliberately excludes.

**Key takeaway**: `## What` / `## Why` / `## How this was checked` / `## Not in scope` is a small,
repeatable template that forces a description toward one concern, one sentence, every time.

**Why It Matters**: a PR description that lists five unrelated changes forces the reviewer to
reconstruct the actual scope from the diff itself -- exactly the cognitive tax co-06's "one PR, one
concern" rule exists to remove. `## Not in scope` is the cheapest line in the template and the one
most PRs skip, even though it is what stops "while I was in there" scope creep before it starts.
