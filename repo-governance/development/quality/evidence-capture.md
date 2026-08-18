---
title: "Evidence Capture Convention"
description: Standards for capturing and organizing testing evidence (screenshots, curl outputs, console logs) in plan folders and delivery.md during plan execution
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
when_to_use: "Use when capturing, naming, or referencing testing evidence during plan execution."
---

# Evidence Capture Convention

This convention defines where testing evidence lives and how it must be named, formatted, and referenced from `delivery.md` so a reviewer can verify a claim without re-running the test.

## Documents

- [Principles and Conventions Implemented/Respected](./evidence-capture/principles-and-conventions-implemented-respected.md) — Principles and conventions this convention implements. Use when tracing this convention to the principles/conventions behind it.
- [The Rule](./evidence-capture/the-rule.md) — The rule requiring evidence capture for testing performed during plan execution. Use when you need the exact wording of the evidence-capture rule.
- [Evidence Folder Location](./evidence-capture/evidence-folder-location.md) — Where captured evidence lives within a plan folder. Use when deciding where to save a screenshot or curl output during plan execution.
- [What Goes Where](./evidence-capture/what-goes-where.md) — Which evidence type goes in which file/folder, and what delivery.md must reference. Use when unsure which evidence file to save a specific artifact into.
- [Screenshot Conventions](./evidence-capture/screenshot-conventions.md) — Naming, format, and content requirements for captured screenshots. Use when naming or capturing a screenshot as plan evidence.
- [curl / API Evidence Conventions](./evidence-capture/curl-api-evidence-conventions.md) — How to capture and format curl/API evidence during plan execution. Use when capturing curl or API-response evidence for a plan.
- [Locale Testing Evidence Requirements](./evidence-capture/locale-testing-evidence-requirements.md) — The evidence bar for locale/i18n testing across supported languages. Use when verifying a locale-sensitive feature and capturing its evidence.
- [What plan-execution-checker Validates](./evidence-capture/what-plan-execution-checker-validates.md) — What the plan-execution-checker agent inspects in captured evidence. Use when you need to know what evidence the plan-execution-checker gate inspects.
- [Examples](./evidence-capture/examples.md) — Worked examples of correctly captured evidence. Use when you need a concrete example of properly captured evidence.
- [Relationship to Other Conventions](./evidence-capture/relationship-to-other-conventions.md) — How this convention relates to manual-behavioral-verification and other quality conventions. Use when deciding whether evidence capture or another convention governs a specific check.
- [Related Documentation](./evidence-capture/related-documentation.md) — Cross-references to related verification and plan conventions. Use when you need a related convention on verification or plan structure.
