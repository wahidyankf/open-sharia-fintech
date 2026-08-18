---
title: "Mechanize Cross-File Invariants"
description: When a rule must hold across more than one file, generate the dependent file(s) from a single declared source and validate the result, rather than stating the rule in prose and trusting hand-sync
category: explanation
subcategory: development
tags:
  - generate-and-validate
  - drift
  - automation
  - governance
created: 2026-08-07
when_to_use: Use when a rule, value, or structure must stay identical across two or more files, before writing it as prose you'd have to remember to keep in sync by hand.
---

# Mechanize Cross-File Invariants

If a rule must stay true across more than one file, don't state it in prose and rely on
contributors to keep the files in sync by hand. Generate the dependent file(s) from one declared
source, and validate the generated output against that source. A rule with no mechanism decays
silently; a rule enforced only by a human remembering to update every copy will eventually be
forgotten in at least one.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: hand-sync drift
  is a recurring symptom with one root cause — no single source of truth. Generating from a
  declared source removes the recurring symptom instead of re-fixing each instance it produces.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: a
  generate-and-validate pipeline is the direct application of this principle to cross-file
  consistency specifically.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: one
  declared source plus a generator is simpler to reason about than N independently-maintained
  copies that are supposed to agree but have no mechanism guaranteeing it.

## Contents

- [The Rule](./mechanize-cross-file-invariants/the-rule.md) — the four-step generate-and-validate procedure.
- [Prior Art In This Repository](./mechanize-cross-file-invariants/prior-art-in-this-repository.md) — four cross-cutting invariants this pattern already governs.
- [Examples](./mechanize-cross-file-invariants/examples.md) — a PASS and a FAIL worked example.
- [Scope and Related Documentation](./mechanize-cross-file-invariants/scope-and-related-documentation.md) — where this practice applies, and links to related conventions.
