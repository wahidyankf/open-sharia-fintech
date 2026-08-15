---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

Which seam owns authority? The permission and sandbox boundary, not the model loop.

## Calculation practice

Allocate a 12k-token budget across task, retrieved files, tool results, and a reserve; state the
compaction trigger.

## Scenario judgment

A request asks to read `../.env`. Deny it, record the reason, and keep the secret out of context.

## Design exercise

Draw the approval path from tool request through policy, sandbox, audit record, and observation.

## Automaticity checklist

- [ ] I can make a fake-provider loop deterministic.
- [ ] I can stop a run on budget, approval denial, or a final answer.
