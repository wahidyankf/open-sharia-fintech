---
title: "The Completeness Checklist"
description: "The checklist to verify before declaring a feature change complete."
category: explanation
subcategory: development
tags:
  - feature-completeness
  - specs
  - contracts
  - testing
  - documentation
  - quality
created: 2026-04-04
when_to_use: "Use as a final check before declaring a feature change done."
---

# The Completeness Checklist

Before declaring a feature change complete, verify:

- [ ] **Gherkin specs** reflect the new/changed/removed behavior
- [ ] **OpenAPI contracts** reflect the new/changed/removed API surface (if applicable)
- [ ] **Unit tests** cover the new/changed logic (coverage thresholds met)
- [ ] **Integration tests** cover cross-component interactions (if applicable)
- [ ] **E2E tests** cover user-facing flows (if applicable)
- [ ] **Documentation** reflects the new/changed behavior (READMEs, docs/, inline)
- [ ] **C4 diagrams** reflect architectural changes (if applicable)
- [ ] **specs/README.md** updated (if project structure changed)
