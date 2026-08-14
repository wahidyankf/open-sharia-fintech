---
title: "Rate Limit Budget Facts"
description: The GitHub API rate-limit quota, reset window, and why a tight poll loop or gh run watch exhausts it.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use when estimating whether a polling approach will exhaust the GitHub API rate limit.
---

# Rate Limit Budget Facts

Understanding the budget prevents accidental exhaustion.

| Parameter            | Value                                                                          |
| -------------------- | ------------------------------------------------------------------------------ |
| Quota                | 5,000 requests/hour per authenticated user                                     |
| Reset window         | Rolling 1 hour from the first request                                          |
| When exhausted       | HTTP 403 on all subsequent `gh` commands                                       |
| Reset timing         | Top of the next hour from first call                                           |
| Single `gh run view` | 1 request per invocation                                                       |
| `gh run watch`       | Polls internally every ~3s; **prohibited for CI monitoring** (stream-watching) |

A tight loop with no sleep issues hundreds of requests per minute. At 200 calls/minute, the 5,000-request quota exhausts in 25 minutes. **`gh run watch` on a 30-minute CI run also exhausts the quota** — it polls ~3 times/minute for 30 minutes = ~90 calls just for watching. Combined with triggers and other list calls this crosses 5,000 quickly. Any `gh` command — list, trigger, view — then returns HTTP 403 until the window resets.
