---
title: "Standard 5 — Status-Update Cadence While Background Agents Run"
description: "Covers mixed-batch cadence, why reporting cadence differs from polling cadence, and the floor and ceiling on status updates."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when deciding how often to post a status update while background agents are running.
---

# Standard 5 — Status-Update Cadence While Background Agents Run

While one or more background agents are in flight, or while task-list items are active, the main agent MUST post a visible status update to the user in the main thread. The interval between updates is determined by the **kind** of work being awaited, not by a single fixed number:

| Kind of Work      | Examples                                                              | Reporting Interval  |
| ----------------- | --------------------------------------------------------------------- | ------------------- |
| GitHub CI-related | Actions runs, PR checks, workflow conclusions, post-push verification | Every **3 minutes** |
| Generic           | Subagent batches, refactors, doc sweeps, test runs — everything else  | Every **5 minutes** |

## Mixed Batches Take the Tighter Cadence

When a batch contains both CI-related and generic in-flight items, the whole batch reports at the tighter **3-minute** cadence. Rationale: the CI item is the one that can go red and block delivery, so it sets the pace for the batch even when most items in flight are generic.

## Reporting Cadence Is Not Polling Cadence

This is the most important distinction in this Standard. Standard 5 governs how often the main agent **speaks to the user** — it changes nothing about how often the main agent **checks** anything. Two existing polling rules stay exactly as they were:

- The CI/GitHub-Actions polling floor of never faster than once every 2 minutes (see [CI Monitoring Convention](../../workflow/ci-monitoring.md)) is unchanged.
- Standard 2's 3-minute stuck-detection mtime poll (above) is unchanged.

The normal consequence: for CI work, the main agent polls every 2 minutes but reports every 3, so not every poll produces a user-visible message. For generic work, the main agent polls for stalls every 3 minutes (Standard 2) but reports every 5, so not every stall-detection poll produces a user-visible message either.

## Floor and Ceiling

The interval is both a **floor on chattiness** and a **ceiling on silence**. Updating more often than the interval is noise — it buries the signal the user actually needs under status chatter. Letting more than one interval elapse while work is in flight reads to the user as a stall, even when the work is healthy.
