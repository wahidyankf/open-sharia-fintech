---
title: "Real-World Context"
description: The historical incident that prompted this convention — 50+ instances of public ayokoding.com URLs found in docs/explanation/.
when_to_use: Use when you need the origin story or impact rationale behind this convention, e.g. in a proposal to extend or relax it.
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

# Real-World Context

**Historical issue:** This convention was created after discovering 50+ instances where public web links (`https://ayokoding.com/...`) were incorrectly used instead of relative paths in Java, Spring Framework, and Spring Boot explanation documentation.

**Impact:** These external URLs created false external dependencies for repository-internal content, breaking offline development workflows and obscuring the repository structure.

**Resolution:** Systematic replacement of all `https://ayokoding.com/` URLs in docs/explanation/ with correct relative paths following this convention.
