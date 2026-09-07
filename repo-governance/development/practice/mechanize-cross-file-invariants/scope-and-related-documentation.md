---
description: Where this practice applies and where it deliberately does not, plus links to related conventions and principles
when_to_use: Use when deciding whether a specific case of divergence falls under this practice, or to find the related conventions and principles.
---

# Scope and Related Documentation

## Scope

This practice applies whenever a rule, value, or structure must hold identically across two or
more files or surfaces within a single repository. It does not apply to:

- Content that is _intentionally_ allowed to diverge per repo (see, for example, the
  [SDLC Gate Standard's Allowed Divergence section](../../../../docs/reference/sdlc-gate-standard.md#allowed-divergence))
  — mechanizing an invariant that isn't actually invariant produces false-positive drift reports.
- A rule stated once, with no second location that must agree with it — there is nothing to
  mechanize until a second copy exists or is planned.

## Related Documentation

- [File-Touch Discipline](../file-touch-discipline.md) — the same-commit rule for generated harness
  mirrors, a specific instance of this general practice
- [PR Merge Protocol](../../workflow/pr-merge-protocol.md) — resolving merge conflicts in generated
  files at the source, not in the generated artifact
- [Root Cause Orientation Principle](../../../principles/general/root-cause-orientation.md) — the
  foundational principle this practice operationalizes for cross-file consistency
- [Automation Over Manual Principle](../../../principles/software-engineering/automation-over-manual.md)
  — the general principle this practice specializes for cross-file consistency
