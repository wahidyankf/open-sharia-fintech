---
title: "Anti-Pattern — Echo and No-Op Test Targets"
description: "Why an inapplicable test boundary must be omitted instead of represented by a placeholder"
category: explanation
subcategory: development
tags: [nx, targets, testing]
created: 2026-02-23
when_to_use: "Use when a project lacks an applicable runtime or coverage layer."
---

# Anti-Pattern — Echo and No-Op Test Targets

An echo, no-op, literal-success, or duplicate target falsely reports that a test boundary exists.
Omit an inapplicable `test:integration`, `test:e2e`, or matching static coverage target and document
the reason in the project README.

Unit is different: every behaviour owner must provide real Unit proof. A dedicated E2E project is
not a behaviour owner and therefore omits Unit rather than adding a placeholder. Workspace-wide
commands rely on Nx's normal target selection; they do not require every project to declare every
target.
