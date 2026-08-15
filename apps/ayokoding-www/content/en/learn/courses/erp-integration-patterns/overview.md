---
title: "Overview"
date: 2026-08-16T00:00:00+07:00
draft: false
weight: 1
---

## Why this exists

ERP integrations must use versioned contracts, accountable source ownership, idempotent consumption, correlation, retries, and observable delivery. A consumer should never depend on a source module's private tables.

## Silent-failure check

### What still balances while being wrong

An integration can eventually deliver every message while duplicate processing creates two business effects. The observable signal is a repeated correlation or source identity without an idempotency decision.
