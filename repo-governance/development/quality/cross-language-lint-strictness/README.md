---
description: "Uniform warning-and-above lint threshold across every language and artifact type in this repository."
when_to_use: "Read this index to find the right Cross-Language Lint Strictness child document."
---

# Cross-Language Lint Strictness

- [Policy](./policy.md) — The warning-and-above threshold, two enforcement points, toolchain convergence, clean-then-gate rollout, and documented-waivers-only rule for every cross-language lint gate. Use when adding a new lint gate, deciding its failure threshold, or documenting a lint-rule waiver.
- [Gated standards](./gated-standards.md) — The table of every currently-gated artifact type, its linter, threshold/config, and CI job. Use when checking which linter and CI job gates a given artifact type (shell, Dockerfile, GitHub Actions YAML, F#, Markdown, formatting).
