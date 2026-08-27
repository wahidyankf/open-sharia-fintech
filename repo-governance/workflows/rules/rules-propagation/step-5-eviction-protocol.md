---
title: "Step 5: Eviction Protocol"
description: How the workflow frees room on a full instruction surface by relocating a resident entry into a governance layer, in the same delivery as the admission.
when_to_use: Use when a rule has passed the admission test's necessity condition but the destination has no budget headroom.
---

# Step 5: Eviction Protocol

The instruction surface is a fixed-size cache. It is normal for it to be full, and every admission
to a full surface displaces something. This step runs only when Step 4 admitted a rule on necessity
and found no room.

## Choose the Eviction

Rank the destination's current residents by the same necessity condition the candidate had to pass,
and evict the weakest — the entry most reachable by other means. Strong signals of a weak resident:

- It already links out to a governance document that states it more fully. The instruction-surface
  copy is a pointer wearing a rule's clothing.
- It describes rather than binds — orientation text, a tool blurb, a status note.
- Its subject has an owning document elsewhere that would be the first place anyone looked.

Never evict by age, position, or convenience. "It was here first" is not a necessity argument, and
neither is "it is at the bottom".

## Relocate, Do Not Delete

An evicted entry is **moved**, not dropped. Its substance lands in the governance layer that owns
its subject, and the instruction surface keeps at most a link where the entry stood, when a link is
still warranted. Compression in place counts as eviction only when the compressed form still
states the whole obligation.

Deleting an evicted entry outright is permitted only when Step 3 already found it superseded, and
then it is recorded as a supersession rather than an eviction.

## Same Delivery

The eviction and the admission land in the **same** PR. An admission whose eviction is deferred
leaves the surface over budget, and a deferred eviction that never happens turns a fixed-size cache
into an unbounded one.

## Verify the Arithmetic

After the eviction and the admission, measure the destination's word count directly rather than
predicting it, and measure the resolved instruction tree as well — a shim and its canonical file
share a combined ceiling, so freeing room in one can still leave the tree over budget.

## Record

The manifest records every eviction: what moved, where it went, and which admission paid for it.

## Related Documents

- [Step 4: Placement](./step-4-placement-decision.md) — what triggers this step.
- [Safety Features](./safety-features.md) — the guards on relocation.
