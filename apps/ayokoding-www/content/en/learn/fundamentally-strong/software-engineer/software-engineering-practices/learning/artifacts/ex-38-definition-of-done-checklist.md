---
title: "Artifact: A Team Definition of Done, Applied"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 78
---

> ex-38 &middot; exercises co-21 &middot; a written checklist, applied to a real PR.

**Team Definition of Done**:

```text
[ ] Tests pass locally AND in CI (co-08)
[ ] Code reviewed and approved by at least one other engineer (co-05)
[ ] Docs (README/docstrings) updated in the SAME PR, if behavior changed (co-17)
[ ] Changelog entry added under [Unreleased], if user-facing (co-04)
[ ] No new required-check failures, no unresolved review comments
```

**Applied to PR #142 (feat(auth): add token refresh)**:

```text
[x] Tests pass locally AND in CI              -- pytest -k refresh_token green, ci/test green
[x] Code reviewed and approved                -- reviewer-jane approved (Example 13)
[x] Docs updated in the same PR               -- README's Client section updated alongside auth.py
[x] Changelog entry added                     -- "Added" entry under [Unreleased] (Example 5)
[x] No unresolved comments                    -- the one request-changes comment was addressed
```

**Verify**: the PR is marked done only once every item is checked -- at the point where 4 of 5 items
were checked (before the changelog entry existed), the PR is correctly NOT yet done, satisfying
co-21's gating rule.

**Key takeaway**: "done" is a checklist result, not a feeling -- a PR that is reviewed, tested, and
green but has no changelog entry is not done yet, by this team's own explicit definition.

**Why It Matters**: an implicit, unwritten Definition of Done lets "done" mean something different
to every engineer (some skip the changelog, some skip docs) -- writing it down, per the Scrum
Guide's own framing, is what makes "done" a shared, checkable fact instead of an individual opinion.
