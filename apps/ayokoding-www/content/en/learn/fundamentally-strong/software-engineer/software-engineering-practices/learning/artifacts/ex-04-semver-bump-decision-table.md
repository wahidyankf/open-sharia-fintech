---
title: "Artifact: SemVer Bump Decision Table"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 44
---

> ex-04 &middot; exercises co-03 &middot; SemVer 2.0.0's own backward-compatibility test, applied to
> three real changes.

SemVer 2.0.0 ties a version bump to exactly one question per change: does this change break an
existing caller's reasonable expectations? Answering that question, one change at a time, is the
whole discipline -- there is no fourth option and no partial credit.

| #   | Change                                                                                                 | Backward compatible?                                                                                | SemVer bump | Why                                                                                                                                 |
| --- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Fix a bug where `parse_date("")` raised `IndexError` instead of returning `None`                       | Yes -- callers relying on the old crash were relying on a bug, not a contract                       | **PATCH**   | A backward-compatible bug fix is SemVer's own definition of PATCH.                                                                  |
| 2   | Add an optional `timeout: float = 30.0` keyword argument to `fetch(url)`                               | Yes -- every existing call site, with no `timeout` argument, still compiles and behaves identically | **MINOR**   | A backward-compatible ADDITION (a new, optional capability) is SemVer's own definition of MINOR.                                    |
| 3   | Remove the public `Client.legacy_connect()` method (superseded by `Client.connect()` two releases ago) | No -- any caller still using `legacy_connect()` now fails to import or call it at all               | **MAJOR**   | Removing a public API is an incompatible change under SemVer's own definition of MAJOR, no matter how long it was deprecated first. |

**Verify**: each row's bump matches SemVer's own "was this change backward compatible" test -- row 1
(a fix) is PATCH, row 2 (an addition) is MINOR, row 3 (a removal) is MAJOR, and each justification
names the specific compatibility property, not just the change's category label.

**Key takeaway**: SemVer never asks "how big does this feel" -- it asks one binary question,
compatibility, and the bump follows mechanically from the answer.

**Why It Matters**: teams that eyeball version bumps ("this feels like a minor tweak") routinely
under-bump breaking removals and over-bump safe additions, both of which mislead every downstream
consumer's own dependency-pinning strategy (a caret range like `^1.2.0` trusts that no MAJOR bump
means no breakage). The table above is the whole trick: reduce every change to the one
compatibility question SemVer actually asks, and the bump stops being a judgment call.
