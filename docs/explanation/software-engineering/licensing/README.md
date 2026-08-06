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

- [Why MIT? — Strategic Rationale](mit-license-rationale.md) - Why this repository uses the MIT License: business risks accepted, benefits of full openness, and the market context (building-block economy vs. feature-monopoly model).
- [Licensing Decisions](licensing-decisions.md) - Analysis and decisions for notable dependencies: Liquibase FSL-1.1-ALv2, Hibernate LGPL-2.1, sharp-libvips LGPL-3.0, and Logback EPL-1.0/LGPL-2.1. Includes the quarterly audit schedule.
- [Production Dependency Compatibility](dependency-compatibility.md) - Historical audit (2026-04-04) of production dependency licenses, including LGPL elimination and MPL-2.0 analysis.

## Related Documentation

- [Database Audit Trail Pattern](../../../../repo-governance/development/pattern/database-audit-trail.md) - Migration tool selection per language ecosystem
- [Software Engineering Index](../README.md) - All software engineering documentation
