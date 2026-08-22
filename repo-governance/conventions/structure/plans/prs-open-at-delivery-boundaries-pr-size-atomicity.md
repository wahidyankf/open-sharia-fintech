---
title: "Bounding PR Size — The Atomicity Exception (Rule 5)"
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

# The Atomicity Exception (Rule 5)

[Bounding PR Size](./prs-open-at-delivery-boundaries-pr-size.md) rule 1 splits a sweep by surface
and rule 4 bounds each slice at ≤400 changed lines and ≤20 hand-authored files. This is the single
case where those yield.

## The Rule

**A slice must be self-consistent on `main` the moment it merges.** Surfaces split cleanly only
when each states a rule the others do not. Where one rule is stated on two surfaces — a
`repo-governance/` convention and the `.claude/` binding that executes it — those two surfaces are
**one slice**, merged together, even past rule 4's bound. A size bound never outranks correctness:
a `main` stating one rule two contradicting ways is worse than a large PR.

## What the Exception Does Not Carry

It admits **only the paired surfaces, and only for rules this PR changes**. Nothing else rides
along on the strength of it — an unrelated fix in a file the slice happens to touch is still scope
creep, and rules 1-3 still bound what enters. Rule 4 stays the bound for every other PR.

**A surface is a rule-1 category, not a directory.** Governance text is one surface however many
subdirectories of `repo-governance/` a rule spans; agents plus their generated mirrors are one
surface covering all of `.claude/` and `.agents/`. The exception pairs exactly **two** of those
categories. Counting directories instead would make almost any change look like a many-surface
sweep and read this exception as a blanket exemption, which it is not.

Expect this to fire on most rule changes rather than rarely: a rule worth enforcing is usually
stated once in governance and again in the binding that executes it. That is the intended reading,
not a loophole — the exception grows a PR only along the seam where splitting would break `main`,
and the resulting diff is repetitive by construction, one rule restated per surface, which is what
makes it reviewable at a size rule 4 would otherwise reject.

## Where the Split Is Safe

Between independent surfaces — governance versus specs versus plans — each is separately consistent
and rule 3 bounds the gap to a single merge. Rule 5 marks where it is not, learned empirically: a
`.claude/`-only slice of this very convention drew five reviewer findings, each for contradicting
the `repo-governance/` text the split left behind.

## Declaring It

A PR relying on this exception says so in its body's `## Scope` section, names the two paired
surfaces, and states the size it reached. An undeclared oversized PR is indistinguishable from an
unbounded one.

**Enforcement: none.** No gate checks this; it binds the author.
