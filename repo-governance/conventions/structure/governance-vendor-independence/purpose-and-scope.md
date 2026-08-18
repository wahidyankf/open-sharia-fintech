---
title: "Governance Vendor-Independence — Purpose and Scope"
description: Why governance prose must be vendor-neutral, and exactly which files (repo-governance/, AGENTS.md, CLAUDE.md) this convention governs vs. exempts.
when_to_use: Use when checking whether a file or line falls inside the vendor-independence convention's scope.
category: explanation
subcategory: conventions
tags:
  - conventions
  - governance
  - vendor-independence
  - agents
  - platform-bindings
created: 2026-05-02
---

# Purpose and Scope

## Purpose

`repo-governance/` contains the rules every contributor follows regardless of toolchain. When vendor-specific product names, model names, or path references appear in governance prose, they:

- Exclude contributors using other AI coding agents (Cursor, Codex CLI, Gemini CLI, Copilot, Aider).
- Couple governance correctness to a specific vendor's product lifecycle.
- Create maintenance debt when vendor names or APIs change.

This convention separates **vendor-neutral governance** (the rules) from **platform bindings** (the vendor-specific wiring that executes the rules) by pushing all binding details out of `repo-governance/` and into the appropriate platform-binding directory.

## Scope

**Applies to**: every `.md` file under `repo-governance/`, **plus the canonical root instruction surfaces**:

- `AGENTS.md` — canonical root instruction file (read natively by OpenCode, OpenAI Codex CLI, and other AGENTS.md-aware coding agents). Vendor-neutrality here is the load-bearing surface for cross-vendor behavioral parity.
- `CLAUDE.md` — Claude Code shim. While CLAUDE.md is itself a Claude-Code platform binding artifact (its filename names the vendor by design), its **prose body** must be vendor-neutral by the same standard as `repo-governance/`. Two specific allowances apply:
  - The single-line `@AGENTS.md` import directive is treated as an inline binding directive, not a forbidden vendor term.
  - Vendor-specific clarifications inside CLAUDE.md belong inside ` ```binding-example ` fenced blocks or under a "Platform Binding Examples" heading per the Allowlist Mechanism — never as load-bearing prose.

**Out of scope** (vendor terms are intentionally present here):

- `.claude/` — Claude Code platform binding directory.
- `.opencode/` — OpenCode platform binding directory.
- `docs/reference/platform-bindings.md` — catalog of all platform bindings; references them by necessity.
- `plans/` — planning documents; may reference vendor specifics when discussing implementation details.
