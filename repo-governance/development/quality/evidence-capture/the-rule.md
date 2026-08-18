---
title: "The Rule"
description: "The rule requiring evidence capture for testing performed during plan execution."
category: explanation
subcategory: development
tags:
  - evidence
  - testing
  - screenshots
  - plans
  - verification
  - locale
  - manual-testing
created: 2026-06-20
when_to_use: "Use when you need the exact wording of the evidence-capture rule."
---

# The Rule

**Every manual verification step in a plan MUST produce a committed evidence artifact — inline in
`delivery.md` for text evidence, and in the plan's `evidence/` subfolder for file-based evidence
(screenshots, exported reports). Implementation notes that say "verified manually" without a record
of WHAT was observed are incomplete.**

## Where the Folder Lives

The `evidence/` subfolder belongs to **the plan**, at
`plans/{backlog,in-progress,done}/<slug>/evidence/`, so it travels with the plan into `plans/done/`
on archival. A repo-root `evidence/` is always a misplacement: it outlives the work that produced
it, and nothing links to it.

The only mechanical backstop is a root-anchored `/evidence/` entry in `.gitignore`. Its limits are
deliberate and worth knowing:

- It catches the repo-root case only. A misplaced `apps/<app>/evidence/` is not caught.
- `git add -f` bypasses it.
- It **hides** rather than reports. An agent writing to the repo root gets no error — the files
  simply never stage. If evidence seems to have vanished, check whether it was written to the root.

The leading slash is load-bearing: without it the pattern would also swallow every plan's own
`evidence/` folder and silently stop plans from committing their screenshots.
