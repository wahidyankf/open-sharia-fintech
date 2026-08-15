---
title: "Overview"
date: 2026-08-16T00:00:00+07:00
draft: false
weight: 1
---

## Why this exists

Operational subledgers retain detailed events while a general-ledger control account summarizes their effects. A reliable architecture keeps each generated posting linked to immutable source evidence and supports reconciliation and correction without deleting history.

## Silent-failure check

### What still balances while being wrong

A control account can reconcile to a duplicate source batch. The observable signal is two postings with the same source identity or an idempotency record missing for a repeated request.
