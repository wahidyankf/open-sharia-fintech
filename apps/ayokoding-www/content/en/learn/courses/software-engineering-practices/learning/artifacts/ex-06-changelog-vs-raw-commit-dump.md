---
title: "Artifact: Changelog vs. Raw Commit Dump"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 46
---

> ex-06 &middot; exercises co-04, co-02 &middot; the same release, read two ways.

A changelog and a `git log` cover the same underlying history, but they answer different questions
-- `git log` answers "what happened, in order, to the code," a changelog answers "what changed for
someone using this project." Conventional Commits (co-02) is what makes deriving one from the other
mechanical rather than a rewrite from scratch.

**Raw commit log** (`git log --oneline` for the same release range):

```text
9f2a1e3 fix(auth): correct token expiry off-by-one
7c4d8b1 chore: bump ci runner image
4b7e912 feat(auth): add token refresh
2d1a0f6 refactor(auth): extract token store helper
8f3a1c2 docs: fix typo in README
```

**Curated changelog entry**, derived from the same five commits:

```text
## [1.5.0] - 2026-07-01

### Added

- Token refresh support, so a session no longer requires a full re-login when it expires.

### Fixed

- Corrected a token-expiry calculation that could log a user out one second early.
```

**Verify**: the changelog entry contains zero implementation-only commits (`chore`, `refactor`,
`docs` all vanish -- they carry no user-facing meaning) and rephrases the two user-facing commits
(`feat`, `fix`) as outcomes ("no longer requires a full re-login") rather than restating their
commit subjects verbatim, satisfying co-04's "reads as intent, not raw history" rule.

**Key takeaway**: three of the five commits (`chore`, `refactor`, `docs`) are real, valuable history
-- and correctly absent from the changelog, because none of them changes what a user of the project
can do.

**Why It Matters**: a changelog that just echoes `git log` back at the reader (every `chore` and
`refactor` included) is worse than no changelog at all -- it trains readers to skip it, right when a
real breaking change is buried in commit #14. Curating is the entire value proposition; `git log`
already exists and needs no changelog to reproduce it.
