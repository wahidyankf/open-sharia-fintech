---
title: "Factual Validation Convention — Purpose, Principles, and Scope"
description: Why systematic web-based fact verification matters, the core principles this convention respects, and what content and validation activities are in vs. out of scope.
when_to_use: Use when deciding whether a claim, command, or reference needs web-based verification, or whether a validation task falls under this convention's scope.
category: explanation
subcategory: conventions
tags:
  - factual-validation
  - verification
  - web-research
  - accuracy
  - quality-assurance
created: 2025-12-16
---

# Purpose, Principles, and Scope

## Principles Implemented/Respected

This convention respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Factual validation requires verifying assumptions against authoritative sources rather than proceeding with hidden uncertainty. Makers surface unknown facts, Checkers verify claims using WebSearch/WebFetch tools, and both make verification status explicit rather than implicit.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Web-based verification (WebSearch + WebFetch) automates fact-checking against authoritative sources. Machines verify command syntax, version numbers, and API accuracy - humans focus on content creation and strategic decisions.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Clear confidence classification (PASS: Verified, Unverified, FAIL: Error, Outdated) with explicit verification sources. No hidden assumptions about factual accuracy - every claim is either verified with source citation or marked as unverified.

## Purpose

This convention establishes a systematic methodology for verifying factual correctness in documentation using WebSearch and WebFetch tools. It ensures command syntax, code examples, version numbers, and external references are accurate and up-to-date, reducing documentation errors that mislead users. This methodology provides confidence classification for verified facts.

## Scope

### What This Convention Covers

- **Validation methodology** - How to use WebSearch/WebFetch to verify facts
- **Confidence classification** - [Verified], [Unverified], [Error], [Outdated] labels
- **What to validate** - Command syntax, versions, code examples, API references, external links
- **When to validate** - During content creation, updates, and periodic reviews
- **Validation markers** - How to mark validated content in documentation

### What This Convention Does NOT Cover

- **Link checking** - Covered by dedicated link-checker agents
- **Content accuracy of opinions or recommendations** - This only validates verifiable facts
- **App deployment** - Covered in deployment conventions
- **Automated fact checking** - This is a manual methodology, not automated tooling
