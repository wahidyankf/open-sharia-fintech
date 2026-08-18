---
title: "Cross-Language Lint Strictness"
description: "Uniform warning-and-above lint threshold across every language and artifact type in this repository."
when_to_use: "Read this index to find the right Cross-Language Lint Strictness child document."
---

# Cross-Language Lint Strictness

- [Policy](./policy.md) — The warning-and-above threshold, two enforcement points, toolchain convergence, clean-then-gate rollout, and documented-waivers-only rule for every cross-language lint gate. Use when adding a new lint gate, deciding its failure threshold, or documenting a lint-rule waiver.
- [Gated standards](./gated-standards.md) — The table of every currently-gated artifact type, its linter, threshold/config, and CI job. Use when checking which linter and CI job gates a given artifact type (shell, Dockerfile, GitHub Actions YAML, F#, Markdown, formatting).
- [Configuration files](./configuration-files.md) — Where each lint gate's configuration lives and what it pins or ignores. Use when locating or editing a lint tool's configuration file (.shellcheckrc, .hadolint.yaml, .config/dotnet-tools.json).
- [Rationale and history](./rationale-and-history.md) — Where the cross-repository lint-strictness decision log lives, and related documents. Use when you need the historical rationale for why a specific lint rule is fixed or waived.
