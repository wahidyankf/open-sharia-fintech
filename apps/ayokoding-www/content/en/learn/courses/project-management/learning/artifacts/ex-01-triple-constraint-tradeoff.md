---
title: "Artifact: Trade-off Memo — Aurora Checkout Redesign"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 41
---

> Aurora Checkout Redesign -- trade-off memo -- exercises co-01.

**Request**: add Stripe, PayPal, and Apple Pay provider adapters to scope, six weeks before launch,
with no discussion of budget.

- **Fixed**: launch date (November 15, contractual, tied to the holiday shopping season); original
  core scope (checkout-flow redesign).
- **Absorbs the change**: cost. Two contractor engineers added for six weeks (~$54,000) to build the
  Stripe, PayPal, and Apple Pay provider adapters in parallel with the core redesign, without moving
  the date or cutting any already-committed scope.
- **Alternative considered and rejected**: dropping one of the three providers to stay within the
  existing headcount. Rejected because Finance's own data ranks all three as top-five revenue
  drivers for the holiday quarter -- dropping any one of them defeats the purpose of the request.

**Sign-off**: Aurora PM, Finance liaison, Engineering director.
