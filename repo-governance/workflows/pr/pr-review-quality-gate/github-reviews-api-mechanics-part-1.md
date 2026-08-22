---
title: "PR-Review Quality Gate — GitHub Reviews API Mechanics (Part 1)"
description: "Why the pipeline uses the line-anchored Reviews API instead of top-level comments, and the mechanics of pinning a head SHA, posting one consolidated review, and the REQUEST_CHANGES limitation."
when_to_use: "Use when implementing or debugging the review-posting mechanics, or when confirming why review STATE is always COMMENT even for CRITICAL findings."
---

# GitHub Reviews API Mechanics — Part 1

> **HARD RULE — every review artifact is an inline review thread. `gh pr comment` is never used.**
>
> A review is a **conversation between reviewer and author**, carried as line-anchored threads:
> the coordinator posts one comment per finding, and `pr-review-fixer` **replies on that same
> thread** with its disposition. Two turns, two authors, one thread — never one comment carrying
> both the finding and its resolution.
>
> A top-level comment cannot anchor a line, cannot be replied to as a thread, and cannot be
> resolved — so a review posted that way is invisible to the thread-resolution query the loop uses
> to decide whether it may exit. **It reads as zero findings.** This has been done by mistake on
> this repo; if you find yourself reaching for `gh pr comment`, you are posting the review wrong.

The coordinator (`pr-review-synthesis-maker`) and `pr-review-fixer` interact with the PR through the
GitHub **Reviews API** (line-anchored, independently resolvable review threads). The nine discipline
specialists do not call this API directly — each emits raw findings to the coordinator, which is the
sole poster of record every cycle.

- **Pin one head SHA per pass**: `gh pr view <PR> --json headRefOid` before posting, so every finding
  in a cycle anchors to the same commit.
- **Post exactly ONE consolidated review per cycle**: `gh api` (REST) or `gh api graphql` (GraphQL) to
  create a single pull request review carrying one line-anchored comment per surviving finding, each
  an independently resolvable thread — never one review per specialist.
- **`REQUEST_CHANGES` is structurally unavailable to `pr-review-synthesis-maker` (HARD — do not gate
  on review STATE)**: `gh` authenticates as the PR author under this repo's current identity posture,
  and GitHub rejects `REQUEST_CHANGES` on one's own pull request. Every review this workflow posts
  therefore lands with STATE `COMMENT`, including reviews that carry CRITICAL blocking findings.
  **Any gate that reads GitHub's review state instead of the finding text will read a blocked PR as
  unblocked.** Blocking status is carried by the finding's severity label in the comment body
  (`CRITICAL` / `HIGH`), never by the review's STATE field. Consumers MUST parse severity from
  comment text. This limitation disappears only when a dedicated bot/GitHub App identity is
  provisioned — see the two-pager idea brief
  [`plans/ideas/pr-review-bot-identity.md`](../../../../plans/ideas/q2-not-urgent-important/pr-review-bot-identity.md).
- **List unresolved threads**: a `gh api graphql` query using `reviewThreads(isResolved: false)` — the
  fixer never relies on top-level PR comments for state, only on review-thread resolution status.
  Each thread's comment `databaseId` maps to the REST `comment_id` used when replying.

Continued in [GitHub Reviews API Mechanics — Part 2](./github-reviews-api-mechanics-part-2.md).
