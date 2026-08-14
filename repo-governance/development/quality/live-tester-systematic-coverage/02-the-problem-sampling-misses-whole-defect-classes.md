---
title: "The Problem: Sampling Misses Whole Defect Classes"
description: "Why sampling-based live testing misses entire defect classes."
category: explanation
subcategory: development
tags:
  - testing
  - live-testing
  - usability
  - ux
  - quality
  - systematic
created: 2026-06-22
when_to_use: "Use when deciding whether a live-test pass can sample instead of enumerate."
---

# The Problem: Sampling Misses Whole Defect Classes

The cost-of-living calculator work is the concrete case that motivated this document. The three
testers ran approximately six rounds across that feature and captured more than 40 findings. Yet
after all six rounds, a human found defects the testers had never flagged:

- A shared control (the city/country filter) had no effect on one tab's output while working
  correctly on another. No tester had exercised that control on every tab.
- Inputs were not persisted in the URL, so reload discarded the user's selections. No tester
  had verified the URL-state round-trip for every interactive input.
- An invariant stated in a source-code comment ("URL is the single source of truth") was
  violated by several inputs. No tester had extracted that invariant and checked each input
  against it.
- Multiple controls were styled as raw native elements on some surfaces and as styled components
  on others. No tester had built the full cross-surface consistency matrix.
- Several labels used domain jargon that first-time users could not interpret. No tester had
  scanned every visible label systematically.

None of these gaps resulted from weak testers. They resulted from sampling: each tester exercised
a representative subset of surfaces and controls, which is insufficient for finding cross-surface
inconsistencies and invariant violations. Enumeration closes the gap.
