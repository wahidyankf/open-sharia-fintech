---
title: Cross-Language Lint Strictness
description: Uniform warning-and-above lint threshold across every language and artifact type in this repository.
category: development
subcategory: quality
tags:
  - lint
  - quality
  - ci
created: 2026-06-10
when_to_use: Use when adding, changing, or auditing a lint gate, or checking which tool and threshold gate a given artifact type.
---

# Cross-Language Lint Strictness

This repository enforces a **uniform strictness threshold across every language
and artifact type it ships**: a linter finding at the **warning-and-above** level
fails the build, in both CI and local git hooks. This page indexes the
cross-language lint gates and the policy that binds them.

## Documents

- [Policy](./cross-language-lint-strictness/policy.md) — The warning-and-above threshold, two enforcement points, toolchain convergence, clean-then-gate rollout, and documented-waivers-only rule for every cross-language lint gate. Use when adding a new lint gate, deciding its failure threshold, or documenting a lint-rule waiver.
- [Gated standards](./cross-language-lint-strictness/gated-standards.md) — The table of every currently-gated artifact type, its linter, threshold/config, and CI job. Use when checking which linter and CI job gates a given artifact type (shell, Dockerfile, GitHub Actions YAML, F#, Markdown, formatting).
- [Configuration files](./cross-language-lint-strictness/configuration-files.md) — Where each lint gate's configuration lives and what it pins or ignores. Use when locating or editing a lint tool's configuration file (.shellcheckrc, .hadolint.yaml, .config/dotnet-tools.json).
- [Rationale and history](./cross-language-lint-strictness/rationale-and-history.md) — Where the cross-repository lint-strictness decision log lives, and related documents. Use when you need the historical rationale for why a specific lint rule is fixed or waived.

**See also**: [markdown.md](../quality/markdown.md), [repository-validation.md](../quality/repository-validation.md).

## Principles Implemented/Respected

- [Automation Over Manual](../../principles/software-engineering/automation-over-manual.md) — lint
  policy is enforced by hooks and CI rather than reviewer memory.
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — every
  artifact type uses a declared warning-and-above threshold.
- [Reproducibility](../../principles/software-engineering/reproducibility.md) — local and CI lint
  behaviour use the same checked-in tool configuration.

## Conventions Implemented/Respected

- [Indentation](../../conventions/formatting/indentation.md) and
  [Markdown Formatting](markdown.md) supply formatting rules that their language-appropriate
  deterministic gates enforce.
