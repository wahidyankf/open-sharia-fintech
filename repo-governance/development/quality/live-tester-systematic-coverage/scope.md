---
title: "Scope"
description: "What this practice applies to."
category: explanation
subcategory: development
tags:
  - testing
  - live-testing
  - usability
  - ux
  - quality
  - systematic
created: 2026-06-22
when_to_use: "Use when checking whether this practice applies to a testing pass."
---

# Scope

This practice applies to:

- All runs of `web-exploratory-tester`, `web-usability-tester`, and `web-design-tester` against
  any live web surface in `apps/`.
- All runs of `api-exploratory-tester` against any live REST or GraphQL API in `apps/`.
- All invocations of the `web-ux-test-fixing-planning` workflow.
- The Rule-15 near-end retest required by the
  [User-Facing Delivery Hardening Convention](.././user-facing-delivery-hardening.md) before plan
  archival.

It does not apply to:

- Automated Playwright E2E tests (those follow the [Behaviour-Driven Development](../../behaviour-driven-development.md)).
- API-only verification (covered by [Manual Behavioural Verification](.././manual-behavioural-verification.md)).
- Library-only changes with no UI surface.
