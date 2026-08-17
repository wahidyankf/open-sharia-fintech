---
title: "Relationship to Other Conventions"
description: "How this convention relates to manual-behavioral-verification and other quality conventions."
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
when_to_use: "Use when deciding whether evidence capture or another convention governs a specific check."
---

# Relationship to Other Conventions

- **[Manual Behavioral Verification](.././manual-behavioral-verification.md)** — defines WHAT to verify;
  this convention defines WHERE to record the verification evidence.
- **[User-Facing Delivery Hardening Convention](.././user-facing-delivery-hardening.md)** — Rule 1
  (per-breakpoint, per-locale visual sign-off) and Rule 10 (production visual sign-off before archival)
  both require the evidence trail defined here.
- **[Plans Organization Convention](../../../conventions/structure/plans.md)** — plan folder structure,
  lifecycle (in-progress → done), and the evidence/ subfolder naming.
- **[Temporary Files Convention](../../infra/temporary-files.md)** — evidence/ in a plan folder is NOT a
  temporary file; it is committed and permanent. Use local-tmp/ for scratch work only.
