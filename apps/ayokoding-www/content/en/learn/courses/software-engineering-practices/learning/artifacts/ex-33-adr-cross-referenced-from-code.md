---
title: "Artifact: An ADR Cross-Referenced from Code"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 73
---

> ex-33 &middot; exercises co-18 &middot; the ADR and the code that implements it, each pointing at
> the other.

**`docs/adr/0004-card-balance-document-store.md`**:

```text
# ADR-0004: move card-balance storage to a document store

## Status
Accepted

## Context
Card-balance reads spike 40x during flash sales; PostgreSQL's row-level locking under that load
caused redemption latency to exceed 2s at peak (see incident INC-0091).

## Decision
Move the card_balances table to a document store (keyed by card ID) with eventual-consistency
reads and a compare-and-swap write for redemption, implemented in `balance_store.py`.

## Consequences
Redemption reads no longer contend with writes under load. Trade-off: a redemption immediately
after a top-up can briefly read a stale balance (bounded by the store's own replication lag,
typically <100ms) -- acceptable per the accepted risk documented here.
```

**`balance_store.py`** (the code that implements the decision above):

```python
# balance_store.py
# See docs/adr/0004-card-balance-document-store.md for why this uses a document store
# instead of the PostgreSQL table every other part of this codebase uses.
def read_balance(card_id: str) -> float: ...
def compare_and_swap(card_id: str, expected: float, new: float) -> bool: ...
```

**Verify**: `balance_store.py`'s own header comment names the exact ADR file
(`docs/adr/0004-card-balance-document-store.md`), and that ADR's `## Decision` section names the
exact implementing file (`balance_store.py`) -- each artifact points at the other, satisfying
co-18's cross-reference rule.

**Key takeaway**: an ADR that nobody can find from the code it justifies might as well not exist --
the cross-reference is what turns "why is this weird" into a one-line lookup instead of an
archaeology project.

**Why It Matters**: six months later, an engineer reading `balance_store.py` for the first time and
wondering "why isn't this just a normal table like everything else" finds the answer in one line,
instead of re-litigating (or worse, silently reverting) a decision that was already made deliberately
for a documented reason.
