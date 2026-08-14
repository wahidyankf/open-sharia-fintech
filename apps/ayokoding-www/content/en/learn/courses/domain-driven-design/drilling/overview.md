---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 1
---

## 1. Recall: name the boundary

State the difference between an entity and a value object, then state the invariant that makes an
aggregate boundary necessary. Check yourself: entities have continuity by identity; value objects
have equality by attributes; the aggregate root alone accepts external changes that could violate
its invariant.

## 2. Judgment: choose the smallest aggregate

A buyer can place many orders, and each order must not exceed its own credit limit. Should an
`Order` contain every historical order of a `Customer`? No: make `Order` the root, reference the
customer by `CustomerId`, and handle a cross-order credit policy through an event or reservation
process. Explain why this favors concurrency without silently weakening the rule.

## 3. Code: protect a value

Create a frozen `Money` value object with `amount` and `currency`. Reject a negative amount, and
make addition reject different currencies. Run the test before and after your change; a caller must
never be able to mutate an already valid value object.

## 4. Transfer: translate at a context edge

A legacy CRM calls a customer a `client`, stores names in one field, and represents credit in cents.
Write an ACL that turns that DTO into a Sales `Customer` with `CustomerId`, `Name`, and `Money`.
Keep the legacy DTO out of the Sales domain. Contrast this with a conformist integration, where a
downstream deliberately adopts an upstream published model.

## 5. Self-check: explain the trade-off

Before introducing a repository, event, or bounded context, name the business rule or volatile
integration it protects. If you cannot name one, prefer the simpler model. If a rule spans two
aggregates, explain its asynchronous failure and recovery path instead of pretending one database
transaction protects it.
