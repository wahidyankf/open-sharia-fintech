---
title: "Purpose"
description: Why this convention exists — preventing broken AyoKoding links across offline, CI/CD, and cloned-repository development contexts.
when_to_use: Use when you want to understand what problem this linking convention solves before applying it to a new document.
category: explanation
subcategory: conventions
tags:
  - linking
  - cross-reference
  - relative-paths
  - portability
  - ayokoding-www
created: 2026-02-07
---

# Purpose

This convention ensures documentation references to AyoKoding educational content remain functional and portable across all development contexts. It prevents broken links when:

- Working offline or without internet access
- Testing in local development environments
- Running CI/CD pipelines in isolated containers
- Cloning the repository to different systems
- Migrating domains or hosting infrastructure
- Archiving or backing up documentation

**Key insight**: Content in `apps/ayokoding-www/` is part of the **same repository**. References from `docs/` to AyoKoding content should use repository-internal linking (relative paths), not public web linking (external URLs).
