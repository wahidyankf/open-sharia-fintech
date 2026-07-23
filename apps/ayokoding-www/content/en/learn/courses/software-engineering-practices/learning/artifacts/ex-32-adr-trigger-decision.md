---
title: "Artifact: Which Change Earns an ADR"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 72
---

> ex-32 &middot; exercises co-18 &middot; three changes, only one hard-to-reverse enough to record.

| Change                                                                                    | Hard to reverse?                                                       | Architecturally significant?                              | Earns an ADR? |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------- | ------------- |
| Rename a local variable `d` to `delta` inside `restock()`                                 | No -- a single-file, single-commit revert                              | No -- purely cosmetic, zero external impact               | **No**        |
| Add one `logger.info(...)` line inside the redemption handler                             | No -- trivially removable                                              | No -- observability detail, not a structural choice       | **No**        |
| Swap the primary datastore from PostgreSQL to a document store for the card-balance table | Yes -- touches every read/write path, a data-migration project to undo | Yes -- changes the system's own storage/consistency model | **Yes**       |

**Verify**: only the database swap earns an ADR -- both other changes fail BOTH tests (hard to
reverse, architecturally significant), while the database swap passes both, satisfying co-18's rule
that a routine change does not earn one.

**Key takeaway**: an ADR-worthy decision fails to reverse cheaply AND changes the system's own
structure -- either property alone is not enough (a hard-to-reverse but purely cosmetic rename does
not exist in practice; an easily-reversible architectural experiment behind a flag might not need
one yet either).

**Why It Matters**: writing an ADR for every commit drowns the genuinely significant decisions in
noise, defeating the entire point of having a searchable decision record; the two-question test
(reversibility, architectural significance) keeps the ADR log small enough that someone six months
later will actually read the one that matters.
