---
title: "Bounding PR Size — The Atomicity Exception (PR-Size Rule 5)"
description: "Why a convention and the binding that executes it merge as one slice, past the size bound."
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - pr-review
created: 2026-08-22
when_to_use: "Use when a size split would leave main stating one rule two contradicting ways."
---

# The Atomicity Exception (PR-Size Rule 5)

**Which rule 5?** This is [PR-size rule 5](./prs-open-at-delivery-boundaries-pr-size.md), not
delivery-boundary rule 5; qualify it when citing.

[Bounding PR Size](./prs-open-at-delivery-boundaries-pr-size.md) rule 1 splits a sweep by surface.
[Rule 4](./prs-open-at-delivery-boundaries-pr-size-addition-limits.md) sets the strong 500-code
target plus hard other/document and file caps. Its natural-seam record governs code diffs above 500,
and its narrow plan-document exemption waives only the applicable hard LOC ceiling. Atomicity is
broader: a remaining hard rule-4 bound may yield.

## The Rule

**A slice must be self-consistent on `main` the moment it merges.** Surfaces split cleanly only
when each states a rule the others do not. Where one rule is stated on two — a `repo-governance/`
convention and the `.claude/` binding executing it — those two are **one slice**, merged together,
even past any rule-4 bound. A size bound never outranks correctness: a `main` stating one rule two
contradicting ways is worse than a large PR.

## What the Exception Does Not Carry

It admits **only the paired surfaces, and only for rules this PR changes**. Nothing else rides
along — an unrelated fix in a file the slice happens to touch is still scope creep, and rules 1-3
still bound what enters. Outside atomicity and rule 4's narrow plan-document added-line exemption,
the remaining hard rule-4 bounds stay binding. The 500 code target separately permits a documented
natural-seam exception.

**A surface is a rule-1 category, not a directory.** Governance text is one surface however many
subdirectories of `repo-governance/` a rule spans; agents plus their mirrors are one surface across
`.claude/` and `.agents/`. The exception pairs exactly **two** categories. Counting directories
would make almost any change look like a many-surface sweep and read this as a blanket exemption,
which it is not.

Expect this on many enforced rule changes: a rule often lives in governance and its executing
binding. This is not a loophole. It grows the PR only along the seam where splitting would break
`main`, and the cross-surface repetition keeps that oversized diff reviewable.

## Where the Split Is Safe

Between independent surfaces, each is separately consistent and rule 3 bounds the gap to a single
merge. Rule 5 marks where it is not, learned empirically: a `.claude/`-only slice of this very
convention drew five reviewer findings, each for contradicting the `repo-governance/` text left
behind.

## Declaring It

A PR relying on this exception says so in its body's `## Scope` section, names the two paired
surfaces, and states the size reached. An undeclared oversized PR is indistinguishable from an
unbounded one.

A PR exceeding only the 500 code target uses the natural-seam record instead; it must not claim
atomicity unless splitting would actually make `main` inconsistent.

**Enforcement disposition — unenforced by decision.** Whether two surfaces must land atomically is
a review-time consistency judgment. A relying PR must expose the paired surfaces and reached size
in its `## Scope` section.
