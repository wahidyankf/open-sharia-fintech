---
title: "Orders and Inventory Capstone"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Build a small orders core where `Order` is the aggregate root, `Money` and `Quantity` are immutable
value objects, an in-memory adapter implements a repository port, and placing an order emits a
domain event. A Shipping context receives only a translated integration message through an ACL.

## Steps

1. Start with the tests in `code/tests/`; they pin invalid quantities, credit-limit enforcement,
   event payloads, and ACL translation.
2. Keep the domain package free of storage and transport imports. The repository `Protocol` belongs
   to the domain; the dictionary adapter belongs at the infrastructure edge.
3. Add an `OrderPlaced` event after the root confirms its invariant. Let the application service
   save the root before handing its event to an adapter.
4. Translate Sales terminology to Shipping terminology at the ACL. Shipping receives an order id
   and delivery quantity, not a Sales aggregate object.

## Acceptance criteria

The root prevents an over-limit order; the repository adapter round-trips the root; the event
records the order identity and amount; and the ACL lets no legacy or foreign DTO into the domain.
Run `pytest -q code/tests` from this directory to verify the complete artifact.
