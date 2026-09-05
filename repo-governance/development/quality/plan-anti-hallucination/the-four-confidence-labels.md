---
title: "The Four Confidence Labels"
description: "The four confidence labels for plan claims."
category: explanation
subcategory: development
tags:
  - plans
  - ai-agents
  - factual-validation
  - anti-hallucination
  - web-research
  - verification
created: 2026-05-03
when_to_use: "Use when labeling a claim's confidence."
---

# The Four Confidence Labels

Every non-trivial factual claim written into a plan carries one of four inline labels. Labels are visible in the rendered markdown, not hidden in metadata.

- **`[Repo-grounded]`** — verified against the current commit via `Glob`, `Grep`, `Bash`, or by reading the file. The label may be omitted when the claim appears within a fenced code block whose entire purpose is to quote a repo file (the fence itself is the evidence). Use the label inline whenever a repo path or symbol is named in prose.
- **`[Web-cited]`** — verified against an external source. The claim MUST include the URL and the access date inline. Multi-page research MUST go through `web-researcher` (see Delegation Threshold below).
- **`[Judgment call]`** — explicitly labeled subjective claim. No verification possible because the claim is opinion or expectation. Numeric KPIs that are gut targets (not measurements) MUST use this label.
- **`[Unverified]`** — author flagged the claim as needing verification but proceeded under time pressure. `plan-checker` flags `[Unverified]` claims as MEDIUM findings; `plan-fixer` either verifies and re-labels or escalates to manual review.

Bare unlabeled claims about file paths, versions, APIs, or behaviour are treated as `[Unverified]` by default. Authors SHOULD label proactively rather than rely on the default.
