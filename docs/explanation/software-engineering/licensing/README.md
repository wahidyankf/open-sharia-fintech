---
title: Licensing
description: License analysis and compliance decisions for open-source dependencies used in open-sharia-enterprise
category: explanation
subcategory: licensing
tags:
  - licensing
  - compliance
  - open-source
  - index
created: 2026-03-26
---

# Licensing

This is the decision record for how OSE Platform uses open-source software. Start here when you need the reason behind a licensing choice or the evidence supporting a dependency decision; it is not a substitute for legal advice.

## Why Licensing Documentation?

Open-source licenses set conditions on use, modification, and distribution. Some are permissive (MIT, Apache 2.0); others carry additional obligations (LGPL, EPL) or restrictions (FSL). Recording the decision, its assumptions, and the supporting evidence makes the work reviewable and reduces avoidable risk.

## Documents

- [Why MIT? The Strategic Rationale for Open-Source Licensing](./mit-license-rationale.md) — Explains why the open-sharia-enterprise repository uses the MIT License — the business risks accepted, the benefits that outweigh them, and the market context that informed the decision
- [Licensing Decisions](./licensing-decisions.md) — License analysis and compliance decisions for notable open-source dependencies in open-sharia-enterprise, including Liquibase FSL-1.1-ALv2, Hibernate LGPL-2.1, sharp-libvips LGPL-3.0, and Logback EPL-1.0/LGPL-2.1
- [Production Dependency Compatibility Audit (Historical — 2026-04-04)](./dependency-compatibility.md) — Historical audit (2026-04-04) of all production dependency licenses. Originally scoped to FSL-1.1-MIT compatibility; the project has since reverted to MIT, so FSL-specific concerns no longer apply. Kept as a reference for the LGPL elimination and MPL-2.0 analysis.

## Related Documentation

- [Database Audit Trail Pattern](../../../../repo-governance/development/pattern/database-audit-trail.md) - Migration tool selection per language ecosystem
- [Software Engineering Index](../README.md) - All software engineering documentation
- [Production Dependency Compatibility Audit (Historical — 2026-04-04)](./dependency-compatibility.md) — Historical audit (2026-04-04) of all production dependency licenses. Originally scoped to FSL-1.1-MIT compatibility; the project has since reverted to MIT, so FSL-specific concerns no longer apply. Kept as a reference for the LGPL elimination and MPL-2.0 analysis.
- [Licensing Decisions](./licensing-decisions.md) — License analysis and compliance decisions for notable open-source dependencies in open-sharia-enterprise, including Liquibase FSL-1.1-ALv2, Hibernate LGPL-2.1, sharp-libvips LGPL-3.0, and Logback EPL-1.0/LGPL-2.1
- [Why MIT? The Strategic Rationale for Open-Source Licensing](./mit-license-rationale.md) — Explains why the open-sharia-enterprise repository uses the MIT License — the business risks accepted, the benefits that outweigh them, and the market context that informed the decision
