---
title: "Overview"
date: 2026-08-16T00:00:00+07:00
draft: false
weight: 1
---

## Why this exists

Enterprise documents need named states, guarded transitions, accountable actors, and reversible corrective events. A status field alone cannot prevent invalid business effects.

## Silent-failure check

### What still balances while being wrong

A document can reach a valid-looking status after an unauthorized transition. The observable signal is a state audit missing the actor, guard result, or reason for that move.
